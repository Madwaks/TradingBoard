import json
from pathlib import Path
from typing import Optional, Dict

import requests
from bs4 import BeautifulSoup


class YahooCompanies:
    def __init__(self):
        path = Path("static/data/final_companies.json")
        with open(path, "r") as f:
            self.companies_info = json.load(f)

    def get_company_sector(self):
        updated_companies = []
        for company in self.companies_info:
            if not company["yahoo_url"]:
                continue
            profile_url = company["yahoo_url"] + "/profile"
            sectors = self._get_sectors(profile_url)
            if sectors:
                company.update(sectors)
                updated_companies.append(company)

        with open(Path("static/data/companies_with_sector.json"), "w") as outfile:
            json.dump(updated_companies, outfile, indent=4)

    @staticmethod
    def _get_sectors(profile_url: str) -> Optional[Dict[str, str]]:
        req = requests.get(profile_url)
        soup = BeautifulSoup(req.text, features="html.parser")
        secteur_span = soup.find_all("span", {"class": "Fw(600)"})
        if secteur_span:
            return {"sector": secteur_span[0].text, "sub_sector": secteur_span[1].text}
