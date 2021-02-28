from injector import singleton

from core.models import CompanyInfo
from core.utils.models.company import CompanyInfo as CompanyInfoDC


@singleton
class CompanyInfoFactory:
    def build_company_info(self, company_info_dc: CompanyInfoDC):
        return CompanyInfo(
            yahoo_url=company_info_dc.yahoo_url,
            bourso_url=company_info_dc.bourso_url,
            bfm_url=company_info_dc.bfm_url,
            sector=company_info_dc.sector,
            sub_sector=company_info_dc.sub_sector,
            quotes_file_path=company_info_dc.quotes_file_path,
        )
