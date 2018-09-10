# online_study
本项目主要实现的是一个在线学习网站。可以查看教师，课程，机构等信息。实现全局搜索的功能。

本项目前后端不分离，和慕课网有点类似，比较小众的网站，

使用的数据库是mysql,通信是ajax,使用Django的xadmin系统做管理后台，整体架构比较简洁，清晰。
可以发送邮件，使用的是celery的分布式执行任务，异步实现注册时发送邮件。
部署使用的是nginx 和 uwsgi，
NGINX的好处是负载均衡，反向代理，给网站减轻压力，
request-->nginx-->uwsgi-->django-->uwsgi-->nginx-->response
