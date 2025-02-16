# stock


# mac python 环境
conda base


# 生成依赖

pip install pipreqs
pipreqs ./


# Sealos 自动部署
https://mp.weixin.qq.com/s/RA64X17v3x9oStCP6oxh3w


# stock

```mermaid
graph TD
    A[用户] -->|请求| B[浏览器]
    B -->|请求| C[Django 服务器]
    C -->|请求| D[视图]
    D -->|查询| E[模型]
    E -->|访问| F[数据库]
    D -->|返回| G[模板]
    G -->|响应| B
```


