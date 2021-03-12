import os
from dataclasses import dataclass, field
from pathlib import Path

from injector import singleton, inject
from lazy_property import LazyProperty
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.webdriver import WebDriver


@singleton
class DriverManager:
    @dataclass
    class Configuration:
        download_path: Path
        driver_path: Path
        options: ChromeOptions = field(default_factory=ChromeOptions)

        def __post_init__(self):
            self.options.add_argument("--lang=en-US")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_argument("--ignore-ssl-errors")
            self.options.add_argument("--headless")
            abs_dl_path = os.path.abspath(self.download_path)
            prefs = {"download.default_directory": abs_dl_path}
            self.options.add_experimental_option("prefs", prefs)

    @inject
    def __init__(self, configuration: Configuration):
        self._config = configuration
        self.download_path = Path(self._config.download_path)

    @LazyProperty
    def driver(self) -> WebDriver:
        web_driver: WebDriver = Chrome(
            executable_path=self._config.driver_path,
            chrome_options=self._config.options,
        )
        return web_driver

    def disconnect(self):
        if self.driver:
            self.driver.quit()
