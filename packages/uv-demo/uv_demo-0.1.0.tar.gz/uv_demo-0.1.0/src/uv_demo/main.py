"""Example file."""

import time

from loguru import logger as log
from rich.progress import Progress


def main() -> None:
    """Main function."""

    log.info("Hello UV!")
    with Progress() as progress:
        total: int = 20
        download_task = progress.add_task("[red]Downloading...", total=total)
        for step in range(total):
            time.sleep(0.1)
            if step == total // 2:
                progress.console.print("Halfway there!")
            progress.update(download_task, advance=1)


if __name__ == "__main__":
    main()
