# 项目说明
- python3高效异步爬虫
- 使用`asyncio`和`aiohttp`两个异步模块

# 异步逻辑说明
1. 开始时创建一个等待爬虫url的列表，带有优先级；
2. 每次循环根据指定同时异步爬取多少个url，将1中的列表优先级最高的放入准备爬取列表中；
3. 创建异步任务开始同时爬取准备列表中的url；
4. 爬取成功分析所需要的数据并移除准备列表；
5. 爬取失败加入到等待列表中；
6. 重复执行2-5，直至爬取完成。
