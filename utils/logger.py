import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='meme-fib-monitor'):
    """设置日志记录器"""
    # 创建日志目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建logger对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 创建文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'meme-fib-monitor.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 创建默认logger实例
logger = setup_logger() 