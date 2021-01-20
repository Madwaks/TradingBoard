import os
from pathlib import Path

from injector import singleton, inject
from lazy_property import LazyProperty
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.webdriver import WebDriver


@singleton
class DriverManager:
    @inject
    def __init__(self, download_path: Path):
        self.download_path = download_path
        options: ChromeOptions = ChromeOptions()

        options.add_argument("--lang=en-US")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        abs_dl_path = os.path.abspath(self.download_path)
        prefs = {"download.default_directory": abs_dl_path}
        options.add_experimental_option("prefs", prefs)

    @LazyProperty
    def driver(self) -> WebDriver:
        web_driver: WebDriver = Chrome(
            executable_path=os.getenv("DRIVER_PATH", "stocks_downloader/utils/driver/"),
            chrome_options=self.options,
        )
        return web_driver

    def disconnect(self):
        self.driver.quit()
