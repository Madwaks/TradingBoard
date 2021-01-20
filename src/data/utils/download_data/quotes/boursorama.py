import glob
import logging
import os
import time

from injector import singleton, inject
from selenium.webdriver import ActionChains
from tqdm import tqdm

from data.models.company import Company
from data.utils.driver_manager.driver import DriverManager


@singleton
class QuotationDownloader:
    @inject
    def __init__(self, driver_manager: DriverManager):
        self._driver_manager = driver_manager

    def download_quotations(self, force_download: bool = False) -> None:
        companies = Company.objects.all()

        logging.info(f"{len(companies)} EXISTING COMPANIES")

        for company in tqdm(companies):
            if company.local_file_path and not force_download:
                logging.info(f"[ALREADY DOWNLOADED] <{company.symbol}>")
                continue

            self._driver_manager.driver.get(company.info_url.bourso_url)
            self._download_quotation()

            logging.info(f"[DOWNLOAD] <{company.info_url.bourso_url}> downloaded")

            self._update_company_local_file_path(company)

        self.disconnect()

    def _update_company_local_file_path(self, company: Company) -> None:
        list_of_files = glob.glob(self._driver_manager.download_path / "*")
        latest_file = max(list_of_files, key=os.path.getctime)
        company.local_file_path = latest_file
        company.save()

    def _download_quotation(self):
        full_screen = self._driver_manager.driver.find_element_by_id("fullscreen_btn")
        try:
            time.sleep(1)
            full_screen.click()
        except Exception as e:
            infos = self._driver_manager.driver.find_element_by_class_name(
                "c-table__cell--last"
            )
            self._driver_manager.driver.execute_script(
                "arguments[0].scrollIntoView(true);", infos
            )
            full_screen.click()
        time.sleep(1)
        try:
            five_years = self._driver_manager.driver.find_element_by_xpath(
                '//*[@id="main-content"]/div/section[1]/div[2]/article/div[1]/div/div[1]/div[4]/div[2]/div[1]/div['
                "3]/div[3] "
            )
        except:
            five_years = self._driver_manager.driver.find_element_by_xpath(
                '//*[@id="main-content"]/div/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]'
            )
        five_years.click()
        download_button = self._driver_manager.driver.find_element_by_class_name(
            "c-quote-chart__menu-button--download"
        )
        time.sleep(2)
        action = ActionChains(self._driver_manager.driver)
        action.move_to_element(download_button).perform()
        action.click(download_button).perform()
        time.sleep(5)
