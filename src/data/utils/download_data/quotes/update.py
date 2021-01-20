from injector import singleton

from data.models import Company

import logging
from typing import List, Dict, Tuple, Optional, Any

import dateparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("django")


@singleton
class MissingQuoteDownloader:
    def get_last_quotations(self, company: Company) -> Optional[List[Dict]]:
        if not company.info_url.yahoo_url:
            return None

        all_lines = self._get_missing_data(company)

        if all_lines:
            return [
                self._parse_line(line, company)
                for line in all_lines
                if self._parse_line(line, company)
            ]

    @staticmethod
    def _get_yahoo_history_url(company: Company) -> Tuple[str, str]:
        url = company.info_url.yahoo_url.replace("//fr.", "//") + "/history"

        req_url = requests.get(url)

        return req_url.text, req_url.url

    def _get_missing_data(self, company: Company) -> Optional[List[Dict[str, Any]]]:

        missing_quotes = self._get_missing_quotes(company)

        list_quot_dict = [
            {
                "date": line_content[0].text,
                "open": line_content[1].text.replace(",", ""),
                "high": line_content[2].text.replace(",", ""),
                "low": line_content[3].text.replace(",", ""),
                "close": line_content[4].text.replace(",", ""),
                "volume": line_content[6].text.replace(",", ""),
            }
            for line_content in missing_quotes
            if len(line_content) > 2 and line_content[1].text != "-"
        ]
        return list_quot_dict

    def _get_missing_quotes(self, company: Company):
        all_quote_lines = self._retrieve_yahoo_quote(company)

        missing_quotations = []

        for idx, line in enumerate(all_quote_lines):
            first_elem = line[0].text

            if "Close price" in first_elem:
                missing_quotations = all_quote_lines[:idx]
                break

            parsed_date = dateparser.parse(first_elem)

            if parsed_date.date() == company.last_dated_quotation:
                missing_quotations = all_quote_lines[:idx]
                break

        return missing_quotations

    def _retrieve_yahoo_quote(self, company: Company) -> Optional[List[Dict[str, Any]]]:
        requests_text, requests_url = self._get_yahoo_history_url(company)
        soup = BeautifulSoup(requests_text, features="html.parser")
        all_lines = soup.find_all("tr")
        quotations_lines = [line.find_all("td") for line in all_lines[1:]]
        if len(quotations_lines) < 2 or "lookup" in requests_url:
            return
        return quotations_lines

    @staticmethod
    def _parse_line(quot_dict: Dict[str, str], company: Company) -> Dict[str, Any]:
        return {
            "date": dateparser.parse(quot_dict["date"]),
            "open": float(quot_dict["open"]),
            "high": float(quot_dict["high"]),
            "low": float(quot_dict["low"]),
            "close": float(quot_dict["close"]),
            "volume": 0 if quot_dict["volume"] == "-" else quot_dict["volume"],
            "company": company,
        }
