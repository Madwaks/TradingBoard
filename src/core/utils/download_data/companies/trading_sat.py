import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Tuple

from bs4 import BeautifulSoup

from core.utils.driver_manager.driver import DriverManager
from trade_fox.settings import TRADING_SAT_COMP

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DictCompanyInfo = Dict[str, str]


class TradingSatCompanies(DriverManager):
    def get_companies_list_infos(self) -> List[DictCompanyInfo]:
        companies_info = []

        for page_number in range(1, 7):
            time.sleep(1)
            self.driver.get(
                TRADING_SAT_COMP + f"actions-de-a-z/archives-{page_number}.html"
            )
            html_source = self.driver.page_source
            lines = BeautifulSoup(html_source).find("tbody").find_all_next("tr")
            logging.info(f"Page {page_number} : ")
            for idx, line in enumerate(lines):
                company_name, symbol, url_suffix = self._get_info_from_line(line)
                companies_info.append(
                    {
                        "company_name": company_name,
                        "symbol": symbol,
                        "url_suffix": TRADING_SAT_COMP + url_suffix[1:],
                    }
                )
                logging.info(f"Company {company_name} : <{symbol}>")

        path = Path("static/tradingsat_companies_info.json")
        with open(path, "w") as f:
            json.dump(companies_info, f)
        self.disconnect()

        return companies_info

    @staticmethod
    def _get_info_from_line(line) -> Tuple[str, str, str]:
        company_name = line.find_next("td")
        url_suffix = company_name.find("a")["href"]
        symbol = company_name.find_next("td")
        return company_name.get_text().strip("\n"), symbol.get_text(), url_suffix
