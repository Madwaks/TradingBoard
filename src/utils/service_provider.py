from typing import Type
from django.conf import settings
from injector import Injector, Binder


def _configure_data_downloader(binder: Binder, settings):
    pass


def _configure(binder: Binder):
    _configure_data_downloader(binder, settings)


def _create_injector():
    global _injector
    if _injector is None:
        _injector = Injector(_configure)


def provide(clazz: Type) -> Type:
    _create_injector()

    return _injector.get(clazz)
