import glob
import logging
import os
import time
from typing import NoReturn

from injector import singleton, inject
from selenium.webdriver import ActionChains
from tqdm import tqdm

from core.models.company import Company
from core.utils.driver_manager.driver import DriverManager

SLEEP_TIME = 0.5

logger = logging.getLogger("django")


@singleton
class QuotationDownloader:
    @inject
    def __init__(self, driver_manager: DriverManager):
        self._driver_manager = driver_manager

    def download_quotes_for_company(
        self, company: Company, force_download: bool = False
    ) -> NoReturn:

        if company.info.quotes_file_prefix or not force_download:
            logger.info(f"[ALREADY DOWNLOADED] <{company.symbol}>")
            return
        logger.info(f"[DOWNLOAD] downloading <{company.name}>")
        self._driver_manager.driver.get(company.info.bourso_url)
        self._download_quotation()

        logger.info(f"[DOWNLOAD] <{company.info.bourso_url}> downloaded")

        time.sleep(SLEEP_TIME)
        self._update_company_local_file_path(company)

    def download_quotations(self, force_download: bool = False) -> None:
        companies = Company.objects.all()

        for company in tqdm(companies):
            self.download_quotes_for_company(company, force_download)

        self._driver_manager.disconnect()

    def _update_company_local_file_path(self, company: Company) -> None:
        try:
            list_of_files = glob.glob(
                str((self._driver_manager.download_path / "*").absolute())
            )
            latest_file = max(list_of_files, key=os.path.getctime)
            company.info.quotes_file_prefix = latest_file.split("_")[0]
            company.info.save()
            company.save()
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
