from playwright.sync_api import sync_playwright
import time
import json
import logging
import os

# 配置日志
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, 'xueqiu_crawler.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)

def get_xueqiu_discussions(stock_symbol='贵州茅台'):
    """获取雪球股票讨论数据"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)  # 设置为False以便观察浏览器行为
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 访问雪球页面
            url = f'https://xueqiu.com/k?q={stock_symbol}'
            logging.info(f"正在访问: {url}")
            page.goto(url)
            
            # 等待内容加载并确保页面完全加载
            logging.info("等待页面加载...")
            
            # 尝试多个可能的选择器
            selectors = ['.timeline__item', '.AnonymousHome_home__timeline__item', 
                         '.timeline-item', '.search-home__timeline__item']
            
            selector_found = False
            selected_selector = None
            for selector in selectors:
                try:
                    logging.info(f"尝试选择器: {selector}")
                    # 设置较长的超时时间
                    page.wait_for_selector(selector, timeout=30000)
                    logging.info(f"找到选择器: {selector}")
                    selector_found = True
                    selected_selector = selector
                    break
                except Exception as e:
                    logging.warning(f"选择器 {selector} 未找到: {e}")
            
            if not selector_found:
                logging.error("无法找到任何匹配的选择器，尝试截图保存页面状态")
                page.screenshot(path="xueqiu_page.png")
                logging.info("已保存页面截图到 xueqiu_page.png")
                logging.info("获取页面HTML以便分析")
                html = page.content()
                with open("xueqiu_page.html", "w", encoding="utf-8") as f:
                    f.write(html)
                logging.info("已保存页面HTML到 xueqiu_page.html")
                return []
            
            # 等待网络活动停止
            page.wait_for_load_state('networkidle')
            time.sleep(2)  # 额外等待以确保动态内容加载完成
            
            # 获取讨论列表
            posts = []
            items = page.query_selector_all(selected_selector)
            logging.info(f"找到 {len(items)} 个讨论项")
            
            if len(items) == 0:
                logging.warning("未找到任何讨论项，尝试截图保存页面状态")
                page.screenshot(path="xueqiu_page.png")
                logging.info("已保存页面截图到 xueqiu_page.png")
                logging.info("获取页面HTML以便分析")
                html = page.content()
                with open("xueqiu_page.html", "w", encoding="utf-8") as f:
                    f.write(html)
                logging.info("已保存页面HTML到 xueqiu_page.html")
                return []
            
            for idx, item in enumerate(items):
                try:
                    logging.info(f"正在解析第 {idx+1} 个讨论项")
                    
                    # 尝试多个可能的用户名选择器
                    user_name = None
                    for user_selector in ['.timeline__user-name', '.user-name', '.author-name']:
                        user_name_element = item.query_selector(user_selector)
                        if user_name_element:
                            user_name = user_name_element.inner_text()
                            logging.info(f"找到用户名: {user_name}")
                            break
                    
                    if not user_name:
                        logging.warning(f"第 {idx+1} 个讨论项未找到用户名，跳过")
                        continue
                    
                    # 尝试多个可能的标题选择器
                    title = ""
                    for title_selector in ['.timeline__item__title span', '.item-title span', '.title']:
                        title_element = item.query_selector(title_selector)
                        if title_element:
                            title = title_element.inner_text()
                            logging.info(f"找到标题: {title}")
                            break
                    
                    # 尝试多个可能的链接选择器
                    link = ""
                    for link_selector in ['a.fake-anchor', 'a.title-link', 'a[href]']:
                        link_element = item.query_selector(link_selector)
                        if link_element:
                            href = link_element.get_attribute('href')
                            if href:
                                link = f'https://xueqiu.com{href}' if href.startswith('/') else href
                                logging.info(f"找到链接: {link}")
                                break
                    
                    # 尝试多个可能的内容选择器
                    content = ""
                    for content_selector in ['.timeline__content', '.item-content', '.content']:
                        content_element = item.query_selector(content_selector)
                        if content_element:
                            content = content_element.inner_text()
                            logging.info(f"找到内容: {content[:30]}...")
                            break
                    
                    # 尝试多个可能的时间选择器
                    time_str = ""
                    for time_selector in ['.timeline__time', '.item-time', '.time']:
                        time_element = item.query_selector(time_selector)
                        if time_element:
                            time_str = time_element.inner_text()
                            logging.info(f"找到时间: {time_str}")
                            break
                    
                    # 只有当必要字段都存在时才添加到列表中
                    if user_name and (title or content):
                        post_data = {
                            'user_name': user_name,
                            'title': title,
                            'link': link,
                            'content': content,
                            'time': time_str
                        }
                        posts.append(post_data)
                        logging.info(f"成功添加第 {idx+1} 个讨论项")
                    else:
                        logging.warning(f"第 {idx+1} 个讨论项缺少必要字段，跳过")
                
                except Exception as e:
                    logging.error(f"解析第 {idx+1} 个讨论项时出错: {e}")
                    continue
            
            logging.info(f"总共解析成功 {len(posts)} 个讨论项")
            return posts
        
        except Exception as e:
            logging.error(f"爬取过程中发生错误: {e}")
            # 保存页面截图和HTML以便调试
            try:
                page.screenshot(path="xueqiu_error.png")
                logging.info("已保存错误页面截图到 xueqiu_error.png")
                html = page.content()
                with open("xueqiu_error.html", "w", encoding="utf-8") as f:
                    f.write(html)
                logging.info("已保存错误页面HTML到 xueqiu_error.html")
            except:
                pass
            return []
        finally:
            # 关闭浏览器
            browser.close()

if __name__ == '__main__':
    # 测试代码
    logging.info("开始爬取雪球讨论数据...")
    discussions = get_xueqiu_discussions()
    logging.info(f"爬取完成，获取到 {len(discussions)} 条讨论")
    
    if discussions:
        for i, post in enumerate(discussions):
            logging.info(f"--- 讨论 {i+1} ---")
            logging.info(json.dumps(post, ensure_ascii=False, indent=2))
            logging.info('-' * 50)
    else:
        logging.warning("未获取到任何讨论数据，请检查网络连接或网站结构是否变化")