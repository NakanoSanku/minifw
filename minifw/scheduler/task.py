import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from threading import Thread
from uuid import uuid4, UUID

from loguru import logger


class TaskStatus(Enum):
    NEW = 0
    RUNNING = 1
    COMPLETED = 2


class TaskSchedulerStatus(Enum):
    STOP = 0
    RUNNING = 1
    WAITING = 2


class Task(ABC):
    @abstractmethod
    def __init__(self):
        self.status = TaskStatus.NEW

    @abstractmethod
    def run(self):
        pass

    def get_status(self):
        return self.status

    def reset_status(self):
        self.status = TaskStatus.NEW
        logger.debug(f"Task status Reset to {self.status}")

    def reset(self):
        self.reset_status()

    @abstractmethod
    def before_run(self):
        if self.status == TaskStatus.NEW:
            self.status = TaskStatus.RUNNING
            logger.info(f"Task status Set to {self.status}")

    @abstractmethod
    def after_run(self):
        self.status = TaskStatus.COMPLETED
        logger.info(f"Task status Set to {self.status}")


@dataclass
class TaskQueueItem:
    task: Task
    priority: int
    uuid: UUID = uuid4()
    run_time: datetime = datetime.now()


class TaskQueue:
    def __init__(self) -> None:
        self.queue: list[TaskQueueItem] = []

    def get(self, uuid: UUID):
        for item in self.queue:
            if item.uuid == uuid:
                return item.task

    def put(self, task: Task, priority: int = 0, run_time: datetime = datetime.now()) -> UUID:
        item = TaskQueueItem(task=task, priority=priority, run_time=run_time)
        self.queue.append(item)
        self.sort()
        return self.queue[-1].uuid

    def clear(self):
        self.queue.clear()

    def size(self):
        return len(self.queue)

    def remove(self, uuid: UUID):
        for item in self.queue:
            if item.uuid == uuid:
                self.queue.remove(item)
                return True
        return False

    def get_next_task(self):
        for item in self.queue:
            if item.run_time <= datetime.now() and item.task.get_status() != TaskStatus.COMPLETED:
                return item.task

    def sort(self, reverse: bool = False):
        def get_priority(item: TaskQueueItem):
            return item.priority

        self.queue.sort(key=get_priority, reverse=reverse)


class TaskScheduler:
    def __init__(self, sleep_time: int = 0) -> None:
        self.status = TaskSchedulerStatus.STOP
        self.queue = TaskQueue()
        self.thread: Thread | None = None
        self.daemon_thread: Thread | None = None
        self.daemon_target = None
        self.sleep_time = sleep_time / 1000

    def start(self):
        if self.status == TaskSchedulerStatus.STOP:
            self.status = TaskSchedulerStatus.RUNNING
            self.thread = Thread(target=self.run)
            self.thread.start()

    def run(self):
        if self.daemon_thread is None or not self.daemon_thread.is_alive():
            self.daemon_thread = Thread(target=self.daemon_target, daemon=True)
            logger.info("启动守护线程")
            self.daemon_thread.start()
        while self.status != TaskSchedulerStatus.STOP:
            if self.status == TaskSchedulerStatus.WAITING:
                continue
            task = self.queue.get_next_task()
            if task is None:
                logger.info("任务队列为空")
                self.status = TaskSchedulerStatus.STOP
                return
            task.run()
            time.sleep(self.sleep_time)

    def stop(self):
        if self.status != TaskSchedulerStatus.STOP:
            self.status = TaskSchedulerStatus.STOP
            self.thread.join()
            logger.info("任务调度器已停止")
        else:
            logger.warning("任务调度器未启动")

    def pause(self):
        if self.status == TaskSchedulerStatus.RUNNING:
            logger.info("任务调度器暂停")
            self.status = TaskSchedulerStatus.WAITING
        else:
            logger.warning("任务调度器未启动")

    def resume(self):
        if self.status == TaskSchedulerStatus.WAITING:
            logger.info("任务调度器已恢复")
            self.status = TaskSchedulerStatus.RUNNING
        else:
            logger.warning("任务调度器未暂停")

    def set_daemon(self, target):
        self.daemon_target = target


if __name__ == '__main__':
    class TestTask(Task):
        def __init__(self, s_id):
            super().__init__()  # 必须调用父类初始化方法
            self.s_id = s_id

        def run(self):
            self.before_run()  # 任务开始前调用
            logger.info("TestTask")
            logger.info(self.s_id)
            time.sleep(5)
            self.after_run()  # 任务完成后调用

        def before_run(self):
            super().before_run()  #必须调用父类方法

        def after_run(self):
            super().after_run()  #必须调用父类方法


    def daemon_target():
        while 1:
            logger.info("daemon")
            time.sleep(1)


    t = TestTask(1)
    t2 = TestTask(2)
    s = TaskScheduler()
    s.set_daemon(target=daemon_target)
    s.queue.put(t, 1)
    s.queue.put(t2, 0)

    s.start()
