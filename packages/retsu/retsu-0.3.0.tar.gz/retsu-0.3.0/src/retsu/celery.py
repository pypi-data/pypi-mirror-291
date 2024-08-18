"""Retsu tasks with celery."""

from __future__ import annotations

import logging
import time
import uuid

from functools import wraps
from typing import Any, Callable, Optional

import celery
import redis

from celery import chain, chord, group
from public import public

from retsu.core import (
    MultiProcess,
    RandomSemaphoreManager,
    SequenceSemaphoreManager,
    SingleProcess,
)


class CeleryProcess:
    """Celery Process class."""

    def process(self, *args, task_id: str, **kwargs) -> Any:  # type: ignore
        """Define the process to be executed."""
        chord_tasks, chord_callback = self.get_chord_tasks(
            *args,
            task_id=task_id,
            **kwargs,
        )
        group_tasks = self.get_group_tasks(
            *args,
            task_id=task_id,
            **kwargs,
        )
        chain_tasks = self.get_chain_tasks(
            *args,
            task_id=task_id,
            **kwargs,
        )

        # start the tasks
        if chord_tasks:
            workflow_chord = chord(chord_tasks, chord_callback)
            promise_chord = workflow_chord.apply_async()

        if group_tasks:
            workflow_group = group(group_tasks)
            promise_group = workflow_group.apply_async()

        if chain_tasks:
            workflow_chain = chain(chord_tasks)
            promise_chain = workflow_chain.apply_async()

        # wait for the tasks
        results: list[Any] = []
        if chord_tasks:
            chord_result = promise_chord.get()
            if isinstance(chord_result, list):
                results.extend(chord_result)
            else:
                results.append(chord_result)

        if group_tasks:
            group_result = promise_group.get()
            if isinstance(group_result, list):
                results.extend(group_result)
            else:
                results.append(group_result)

        if chain_tasks:
            chain_result = promise_chain.get()

            if isinstance(chain_result, list):
                results.extend(chain_result)
            else:
                results.append(chain_result)

        return results

    def get_chord_tasks(  # type: ignore
        self, *args, **kwargs
    ) -> tuple[list[celery.Signature], Optional[celery.Signature]]:
        """
        Run tasks with chord.

        Return
        ------
        tuple:
            list of tasks for the chord, and the task to be used as a callback
        """
        chord_tasks: list[celery.Signature] = []
        callback_task = None
        return (chord_tasks, callback_task)

    def get_group_tasks(  # type: ignore
        self, *args, **kwargs
    ) -> list[celery.Signature]:
        """
        Run tasks with group.

        Return
        ------
        tuple:
            list of tasks for the chord, and the task to be used as a callback
        """
        group_tasks: list[celery.Signature] = []
        return group_tasks

    def get_chain_tasks(  # type: ignore
        self, *args, **kwargs
    ) -> list[celery.Signature]:
        """Run tasks with chain."""
        chain_tasks: list[celery.Signature] = []
        return chain_tasks


@public
class MultiCeleryProcess(CeleryProcess, MultiProcess):
    """Multi Process for Celery."""

    ...


@public
class SingleCeleryProcess(CeleryProcess, SingleProcess):
    """Single Process for Celery."""

    ...


def limit_random_concurrent_tasks(
    max_concurrent_tasks: int,
    redis_client: redis.Redis,
) -> Callable[[Any], Any]:
    """Limit the number of concurrent Celery tasks."""

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        semaphore_manager = RandomSemaphoreManager(
            key=f"celery_task_semaphore_random_{func.__name__}",
            max_concurrent_tasks=max_concurrent_tasks,
            redis_client=redis_client,
        )

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Acquire semaphore slot
            acquired = semaphore_manager.acquire()
            if not acquired:
                logging.info(f"Task {func.__name__} is waiting for a slot...")
                while not acquired:
                    time.sleep(0.01)  # Polling interval
                    acquired = semaphore_manager.acquire()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Release semaphore slot
                semaphore_manager.release()

        return wrapper

    return decorator


def limit_sequence_concurrent_tasks(
    max_concurrent_tasks: int,
    redis_client: redis.Redis,
) -> Callable[[Any], Any]:
    """Limit the number of concurrent Celery tasks and maintain FIFO order."""

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        semaphore_manager = SequenceSemaphoreManager(
            key=f"celery_task_semaphore_sequence_{func.__name__}",
            max_concurrent_tasks=max_concurrent_tasks,
            redis_client=redis_client,
        )

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            task_id = str(uuid.uuid4())  # Unique identifier for each task

            # Acquire semaphore slot with FIFO order
            acquired = semaphore_manager.acquire(task_id)
            if acquired:
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # Release semaphore slot
                    semaphore_manager.release()

        return wrapper

    return decorator
