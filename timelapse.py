#!/usr/bin/env python3
"""
Timelapse

Take a timelapse from a RTSP video stream.
"""

__version__ = "0.1.0"

import os
from datetime import datetime

import cv2
import click
import structlog
import time


log = structlog.getLogger()


class Timelapse:
    def __init__(self, url: str, data_dir: str, period: int, debug: int = 0) -> None:
        self.url = url
        self.data_dir = data_dir
        self.period = period
        self.debug = debug

        os.makedirs(data_dir, exist_ok=True)

        assert 10 <= period <= 9999, "Period must be 10-9999 seconds."
        if not url.startswith("rtsp://"):
            raise AttributeError("URL must start with `rtsp://`")

        log.info(f"Timelapse v{__version__}")
        log.info(f"url: {self.url}")
        log.info(f"debug: {self.debug}")
        log.info(f"data dir: {self.data_dir}")
        log.info(f"period: {self.period}")

    def _capture(self):
        self.cap = cv2.VideoCapture(self.url)
        if self.debug >= 3: log.info("capture()")
        _, frame = self.cap.read()
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
        if _ and frame is not None:
            cv2.imwrite(os.path.join(self.data_dir, filename), frame)
            if self.debug >= 1: log.debug(f"captured image {filename}")
        else:
            log.error("Failed to read from video stream.")
        self.cap.release()

    def _close(self):
        if self.debug >= 1: log.info("close()")
        self.cap.release()

    def run(self):
        if self.debug >= 1: log.info("run()")
        while True:
            self._capture()
            log.info(f"sleeping {self.period} seconds")
            time.sleep(self.period)


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option(
    "-o",
    "--data-dir",
    type=str,
    default="data",
    help="The directory for stored files.",
)
@click.option("--period", type=int, default=30, help="Period between frames from video.")
@click.argument("url", type=str)
def main(verbose, data_dir, url, period):
    """
    Take a timelapse from a RTSP video stream.
    """
    tl = Timelapse(url=url, data_dir=data_dir, period=period, debug=verbose)
    tl.run()


if __name__ == "__main__":
    main(auto_envvar_prefix="TIMELAPSE")
