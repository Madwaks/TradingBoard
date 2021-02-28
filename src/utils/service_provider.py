from typing import Type, Optional
from typing import TypeVar

from django.conf import settings, LazySettings
from injector import Injector, Binder

T = TypeVar("T")

_injector: Optional[Injector] = None


def _configure_company_storer(binder: Binder, settings: LazySettings):
    from core.utils.store_data.companies import CompanyImporter

    binder.bind(
        CompanyImporter.Configuration,
        CompanyImporter.Configuration(companies_json_path=settings.COMPANIES_JSON_PATH),
    )


def _configure_data_downloader(binder: Binder, settings: LazySettings):
    from core.utils.driver_manager.driver import DriverManager

    binder.bind(
        DriverManager.Configuration,
        DriverManager.Configuration(
            download_path=settings.DOWNLOAD_STOCKS_PATH,
            driver_path=settings.CHROME_DRIVER_PATH,
        ),
    )


def _configure(binder: Binder):
    _configure_data_downloader(binder, settings)
    _configure_company_storer(binder, settings)


def _create_injector():
    global _injector
    if _injector is None:
        _injector = Injector(_configure)


def provide(clazz: Type[T]) -> T:
    _create_injector()

    return _injector.get(clazz)
