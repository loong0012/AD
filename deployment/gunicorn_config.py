# 阿尔兹海默症诊断系统 - Gunicorn WSGI服务器配置

import os
import multiprocessing

# 服务器socket配置
bind = "0.0.0.0:8000"
backlog = 2048

# Worker进程配置
workers = int(os.environ.get('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = int(os.environ.get('TIMEOUT', 120))
keepalive = 5

# 日志配置
accesslog = '/app/logs/gunicorn_access.log'
errorlog = '/app/logs/gunicorn_error.log'
loglevel = os.environ.get('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程命名
proc_name = 'alzheimer-diagnostic-system'

# 服务器机制
daemon = False
pidfile = '/tmp/gunicorn.pid'
umask = 0o007
user = None
group = None
tmp_upload_dir = '/app/temp/tmp_uploads'

# 钩子函数
def on_starting(server):
    """服务器启动时的钩子"""
    server.log.info("正在启动阿尔兹海默症诊断系统...")

def on_reload(server):
    """服务器重载时的钩子"""
    server.log.info("正在重载服务器...")

def when_ready(server):
    """服务器准备就绪时的钩子"""
    server.log.info("服务器已准备就绪，正在监听端口 8000")

def on_exit(server):
    """服务器退出时的钩子"""
    server.log.info("正在关闭服务器...")

def pre_fork(server, worker):
    """fork worker进程前的钩子"""
    pass

def post_fork(server, worker):
    """fork worker进程后的钩子"""
    server.log.info(f"Worker {worker.pid} 已启动")

def pre_exec(server):
    """重新执行master进程前的钩子"""
    server.log.info("重新执行master进程...")

def pre_request(worker, req):
    """处理请求前的钩子"""
    worker.log.debug(f"{req.method} {req.path}")

def post_request(worker, req, environ, resp):
    """处理请求后的钩子"""
    pass

def worker_int(worker):
    """Worker进程收到SIGINT信号时的钩子"""
    worker.log.info("Worker收到INT信号")

def worker_abort(worker):
    """Worker进程收到SIGABRT信号时的钩子"""
    worker.log.info("Worker收到ABRT信号")