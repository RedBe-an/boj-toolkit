import time
from typing import Optional

from rich.console import Console, RenderableType
from rich.status import Status
from rich.style import StyleType

class BojConsole(Console):
    COLORS = {
        'error': 'red',
        'info': 'deep_sky_blue1',
        'warn': 'yellow',
    }

    def __init__(self):
        super().__init__(log_time=False, log_path=False)

    def log(self, message_type: str, message: str):
        color = self.COLORS.get(message_type, 'white')
        super().print(f"[bold {color}]{message_type.capitalize()}: {message}[/]")

    def status(
        self,
        status: RenderableType,
        *,
        spinner: str = "dots",
        spinner_style: str = "white",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ) -> Status:
        status_renderable = BojStatus(
            f"[bold yellow]{status}",
            console=self,
            spinner=spinner,
            spinner_style=spinner_style,
            speed=speed,
            refresh_per_second=refresh_per_second,
        )
        return status_renderable

class BojStatus(Status):
    def __init__(
        self,
        status: RenderableType,
        *,
        console: Optional[Console] = None,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
        status_term: float = 0.1,
        status_color: str = "[bold yellow]",
    ):
        super().__init__(
            status=status,
            console=console,
            spinner=spinner,
            spinner_style=spinner_style,
            speed=speed,
            refresh_per_second=refresh_per_second,
        )
        self._status_color = status_color
        self._status_term = status_term

    def update(
        self,
        status: Optional[RenderableType] = None,
    ) -> None:
        time.sleep(self._status_term)
        super().update(status=f"{self._status_color}{status}")
        time.sleep(self._status_term)

if __name__ == "__main__":
    console = BojConsole()
    console.log('info', 'hello, world!')
    console.log('warn', 'hello, world!')
    console.log('error', 'hello, world!')

    with console.status("Loading inputs...") as status:
        console.log('info', 'Loading input 1...')
        time.sleep(1)
        console.log('info', 'Loading input 2...')
        time.sleep(1)
