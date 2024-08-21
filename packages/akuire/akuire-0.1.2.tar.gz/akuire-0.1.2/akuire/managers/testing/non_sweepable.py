import asyncio
import dataclasses
from typing import AsyncGenerator

import numpy as np

from akuire.events import (
    AcquireFrameEvent,
    AcquireZStackEvent,
    DataEvent,
    ImageDataEvent,
    ManagerEvent,
    ZChangeEvent,
)
from akuire.managers.base import BaseManager


@dataclasses.dataclass
class NonSweepableCamera(BaseManager):
    exposition_time_is_sleep: bool = True
    __lock = asyncio.Lock()
    __queue = asyncio.Queue()

    async def compute_event(
        self, event: AcquireFrameEvent | ZChangeEvent
    ) -> AsyncGenerator[DataEvent, None]:

        async with self.__lock:
            if isinstance(event, AcquireFrameEvent):
                print("Acquiring frame")
                if self.exposition_time_is_sleep:
                    await asyncio.sleep(event.exposure_time)
                yield ImageDataEvent(
                    data=np.random.rand(
                        1,
                        1,
                        1,
                        512,
                        512,
                    ),
                    device=self.device,
                )

    def challenge(self, event: ManagerEvent) -> bool:
        return isinstance(event, AcquireFrameEvent)

    async def __aenter__(self) -> "NonSweepableCamera":
        self.__lock = asyncio.Lock()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__lock = None
        return None
