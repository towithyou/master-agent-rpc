import logging
import os
from logging.handlers import RotatingFileHandler
from config.conf import LOG_DIR, Platform_system

def get_logger(logger_name=__name__, logfile=None, level=logging.INFO,
               propagate=False, maxBytes=10*1024, backupCount=5,
               encoding=None, fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
               datefmt='%Y/%m/%d %I:%M:%S', stream=True, warn_level=logging.WARN
               ):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # 日志级别
    logger.propagate = propagate  # 传播

    logfile = os.path.join(LOG_DIR, logfile) if logfile else os.path.join(LOG_DIR, logger_name+'.log')
    # logfile = os.path.join(LOG_DIR, logfile+'.log')

    if encoding:
        encoding = encoding
    else:
        if Platform_system == "Windows":
            encoding = 'GBK'
        else:
            encoding = 'utf-8'

    # handle = logging.FileHandler('a.log') # 原始没有日志滚动
    handle = RotatingFileHandler(logfile, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding)
    handle.setLevel(warn_level)  # handler 初始日志级别

    fmt = logging.Formatter(fmt, datefmt=datefmt)
    handle.setFormatter(fmt)  # 为 handler 设置输出格式

    logger.addHandler(handle)

    if stream:
        handle_stream = logging.StreamHandler()
        handle_stream.setLevel(level)
        handle_stream.setFormatter(fmt)
        logger.addHandler(handle_stream)

    return logger

if __name__ == '__main__':
    log = get_logger(logfile='test.log')
    while True:
        log.error('abc')
        log.info('info')