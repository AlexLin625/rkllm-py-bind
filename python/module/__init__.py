import asyncio
from typing import overload
from .rkllm import *

__all__ = [
    "rkllm_create_default_params",
    "RKLLM",
    "RKLLMAsync",
    "RKLLMDataUtils",
]


class RKLLM(RKLLMWrapperBase):
    """
    infer() returns after inference is finished.
    """

    def __init__(self, param: RKLLMParam) -> None:
        param.is_async = False
        super().__init__(param)

    @overload
    def infer(self, prompt: RKLLMInput) -> bool: ...

    @overload
    def infer(self, prompt: str) -> bool: ...

    def infer(self, prompt: str | RKLLMInput) -> bool:
        _prompt: None | RKLLMInput = None

        if isinstance(prompt, str):
            _prompt = RKLLMDataUtils.text_input(prompt)
        else:
            _prompt = prompt

        if _prompt is None:
            return False
        return super().infer(_prompt)


class RKLLMAsync(RKLLMWrapperBase):
    """
    infer() returns immediately and resolves the result later.
    """

    _isRunning: bool
    _buffer: str
    _future: asyncio.Future[str] | None

    def __init__(self, param: RKLLMParam) -> None:
        self._isRunning = False
        self._buffer = ""
        self._future = None

        param.is_async = True
        super().__init__(param)

    @property
    def isRunning(self):
        return self._isRunning

    def infer(self, prompt: RKLLMInput) -> bool:
        raise NotImplementedError("Use inferAsync() for async inference.")

    @overload
    def inferAsync(self, prompt: RKLLMInput) -> asyncio.Future[str]: ...

    @overload
    def inferAsync(self, prompt: str) -> asyncio.Future[str]: ...

    def inferAsync(self, prompt: RKLLMInput | str) -> asyncio.Future[str]:
        _prompt: None | RKLLMInput = None

        if isinstance(prompt, str):
            _prompt = RKLLMDataUtils.text_input(prompt)
        else:
            _prompt = prompt

        if _prompt is None:
            return False

        loop = asyncio.get_event_loop()
        future = loop.create_future()

        if self.isRunning or self._future is not None:
            future.set_exception(Exception("Inference is already running"))
            return future

        self._buffer = ""
        self._future = future
        super().infer(_prompt)
        return future

    def onInferError(self) -> None:
        if self._future is not None:
            self._future.set_exception(Exception("Inference failed"))
            self._future = None
            self._isRunning = False

    def onInferToken(self, token):
        self._buffer += token

    def onInferFinished(self):
        self._isRunning = False
        self._future.set_result(self._buffer)
        self._future = None
