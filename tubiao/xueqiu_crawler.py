from playwright.sync_api import sync_playwright
import time
import json

def get_xueqiu_discussions(stock_symbol='贵州茅台'):
    """获取雪球股票讨论数据"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 访问雪球页面
        url = f'https://xueqiu.com/k?q={stock_symbol}'
        page.goto(url)
        
        # 等待内容加载并确保页面完全加载
        page.wait_for_selector('.timeline__item')
        page.wait_for_load_state('networkidle')
        
        # 获取讨论列表
        posts = []
        items = page.query_selector_all('.timeline__item')
        
        for item in items:
            try:
                # 获取发帖用户名
                user_name_element = item.query_selector('.timeline__user-name')
                if not user_name_element:
                    continue
                user_name = user_name_element.inner_text()
                
                # 获取帖子标题和链接
                title_element = item.query_selector('.timeline__item__title span')
                title = title_element.inner_text() if title_element else ''
                
                link_element = item.query_selector('a.fake-anchor')
                link = ''
                if link_element:
                    href = link_element.get_attribute('href')
                    link = f'https://xueqiu.com{href}' if href else ''
                
                # 获取发帖内容
                content_element = item.query_selector('.timeline__content')
                content = content_element.inner_text() if content_element else ''
                
                # 获取发帖时间
                time_element = item.query_selector('.timeline__time')
                time_str = time_element.inner_text() if time_element else ''
                
                # 只有当必要字段都存在时才添加到列表中
                if user_name and (title or content):
                    posts.append({
                        'user_name': user_name,
                        'title': title,
                        'link': link,
                        'content': content,
                        'time': time_str
                    })
            except Exception as e:
                print(f"解析帖子时出错: {e}")
                continue
                
        # 关闭浏览器
        browser.close()
        return posts

if __name__ == '__main__':
    # 测试代码
    discussions = get_xueqiu_discussions()
    for post in discussions:
        print(json.dumps(post, ensure_ascii=False, indent=2))
        print('-' * 50)