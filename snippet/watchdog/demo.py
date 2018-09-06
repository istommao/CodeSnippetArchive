#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import logging

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        # 记录的格式： 时间 - 消息
                        format="%(asctime)s - %(message)s",
                        # 时间的格式： 年-月-日 时:分:秒
                        datefmt="%Y-%m-%d %H:%M:%S")
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # 获得事件处理对象
    event_handler = LoggingEventHandler()
    # 获得监控事件对象
    observer = Observer()
    # 配置监控对象
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            # 监控时间间隔一秒
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
