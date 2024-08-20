from typing import TYPE_CHECKING, Any, TypedDict, Union, Callable
from ..core import ComponentReturn

if TYPE_CHECKING:
    from .appRunner import AppRunner


class Config(TypedDict, total=False):
    width: str


resolve = Callable[[Any], None]
staticLayout = Union[ComponentReturn, list[ComponentReturn]]


class Page:
    def __init__(self, appRunner: "AppRunner"):
        self.appRunner = appRunner

    def add(
        self,
        layout: Union[
            staticLayout, Callable[[resolve], staticLayout], Callable[[], staticLayout]
        ],
    ) -> Any:
        return self.appRunner.scheduler.ensure_future(self.appRunner.render_ui(layout))

    def download(self, file: bytes, filename: str) -> None:
        self.appRunner.scheduler.create_task(self.appRunner.download(file, filename))

    def set_config(self, config: Config) -> None:
        self.appRunner.scheduler.create_task(self.appRunner.set_config(config))
