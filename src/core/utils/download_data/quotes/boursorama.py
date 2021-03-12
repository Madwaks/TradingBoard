import logging
import os
import time
from dataclasses import dataclass
from os import listdir
from pathlib import Path
from typing import NoReturn, Union

from injector import singleton, inject
from selenium.webdriver import ActionChains
from tqdm import tqdm

from core.models.company import Company
from core.utils.driver_manager.driver import DriverManager
from core.utils.store_data.quotes import QuotationStorer

SLEEP_TIME = 0.5

logger = logging.getLogger("django")


@singleton
class QuotationDownloader:
    @dataclass
    class Configuration:
        quotes_json_folder: Union[Path, str]

    @inject
    def __init__(
        self,
        config: Configuration,
        driver_manager: DriverManager,
        quotes_storer: QuotationStorer,
    ):
        self._driver_manager = driver_manager
        self._quote_factory = quotes_storer
        self._config = config

    @property
    def json_folder_path(self) -> Path:
        return Path(self._config.quotes_json_folder)

    def download_quotes_for_company(
        self, company: Company, force_download: bool = False
    ) -> NoReturn:

        if (
            self.json_folder_path / company.symbol / ".json"
        ).exists() or not force_download:
            logger.info(f"[ALREADY DOWNLOADED] <{company.symbol}>")
            return

        logger.info(f"[DOWNLOAD] downloading <{company.name}>")
        logger.info(f"[DOWNLOAD] <{company.info.bourso_url}> downloading")
        self._driver_manager.driver.get(company.info.bourso_url)
        self._download_quotation()

        time.sleep(SLEEP_TIME)
        local_file_path = self._find_last_downloaded_file_path()

        self._quote_factory.write_quotation_json(
            local_file_path, self.json_folder_path, company
        )

    def download_quotations(self, force_download: bool = False) -> None:
        companies = Company.objects.all()

        for company in tqdm(companies):
            self.download_quotes_for_company(company, force_download)

        self._driver_manager.disconnect()

    def _find_last_downloaded_file_path(self) -> str:
        try:
            list_of_files = [
                file_name.replace(".crdownload", "")
                for file_name in listdir(self._driver_manager.download_path.absolute())
            ]
            file_path = max(list_of_files, key=os.path.getctime)
            return file_path
        except Exception as err:
            raise err

    def _download_quotation(self):
        full_screen = self._driver_manager.driver.find_element_by_id("fullscreen_btn")
        try:
            full_screen = self._driver_manager.driver.find_element_by_id(
                "fullscreen_btn"
            )
            full_screen.click()
        except Exception:
            infos = self._driver_manager.driver.find_element_by_class_name(
                "c-table__cell--last"
            )
            self._driver_manager.driver.execute_script(
                "arguments[0].scrollIntoView(true);", infos
            )
            try:
                full_screen.click()
            except Exception:
                cookies = self._driver_manager.driver.find_element_by_id(
                    "didomi-notice-disagree-button"
                )
                cookies.click()
                time.sleep(SLEEP_TIME)
                full_screen.click()
        time.sleep(SLEEP_TIME)
        try:
            five_years = self._driver_manager.driver.find_element_by_xpath(
                '//*[@id="main-content"]/div/section[1]/div[2]/article/div[1]/div/div[1]/div[4]/div[2]/div[1]/div['
                "3]/div[3] "
            )
        except Exception:
            five_years = self._driver_manager.driver.find_element_by_xpath(
                '//*[@id="main-content"]/div/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]'
            )
        five_years.click()
        download_button = self._driver_manager.driver.find_element_by_class_name(
            "c-quote-chart__menu-button--download"
        )
        time.sleep(SLEEP_TIME)
        action = ActionChains(self._driver_manager.driver)
        action.move_to_element(download_button).perform()
        action.click(download_button).perform()
        time.sleep(SLEEP_TIME)
