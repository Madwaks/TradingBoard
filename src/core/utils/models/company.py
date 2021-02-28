from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin


@dataclass
class CompanyInfo(DataClassJsonMixin):
    yahoo_url: str
    bourso_url: str
    bfm_url: str
    sector: str
    sub_sector: str
    quotes_file_path: str


@dataclass
class Company(DataClassJsonMixin):
    name: str
    symbol: str
    info: CompanyInfo = field(default_factory=CompanyInfo)
