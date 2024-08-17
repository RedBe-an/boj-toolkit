from typing import Optional

import time
import random
from rich.console import Console, RenderableType
from rich.status import Status
from rich.style import StyleType
from rich import print

class BojConsole(Console):
    error_color = "red"
    info_color = "blue"
    warn_color = "yellow"

    def __init__(self):
        super().__init__(log_time=False, log_path=False)

    def error(self, message):
        super().print(f"[bold {self.error_color}]Error: {message}[/]")

    def info(self, message):
        super().print(f"[bold {self.info_color}]Info: {message}[/]")

    def warn(self, message):
        super().print(f"[bold {self.warn_color}]Warning: {message}[/]")
    
    def status(
        self,
        status: RenderableType,
        *,
        spinner: str = "dots",
        spinner_style: str = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ) -> Status:
        status_renderable = BojStatus(
            f"{status}",
            console=self,
            spinner=spinner,
            spinner_style="white",
            speed=speed,
            refresh_per_second=refresh_per_second,
        )
        return status_renderable


class BojStatus(Status):
    status_color: str = "[bold blue]"

    def __init__(
        self,
        status: RenderableType,
        *,
        console: Optional[Console] = None,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ):
        super().__init__(
            status=status,
            console=console,
            spinner=spinner,
            spinner_style=spinner_style,
            speed=speed,
            refresh_per_second=refresh_per_second,
        )

    def update(
        self,
        status: Optional[RenderableType] = None,
        *,
        spinner: Optional[str] = None,
        spinner_style: Optional[StyleType] = None,
        speed: Optional[float] = None,
    ) -> None:
        time.sleep(0.08 + random.uniform(0.1, 0.2))
        super().update(status=f"{self.status_color}{status}[/]")
        time.sleep(0.08 + random.uniform(0.1, 0.2))

