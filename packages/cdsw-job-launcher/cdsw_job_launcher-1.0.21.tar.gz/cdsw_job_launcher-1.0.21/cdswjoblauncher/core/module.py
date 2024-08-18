import importlib
import pkgutil
from abc import ABC, abstractmethod
from inspect import isclass
from typing import List, Iterable, Type, Any

import pip
import logging

from cdswjoblauncher.contract import CdswApp
from cdswjoblauncher.core.error import CdswLauncherException

LOG = logging.getLogger(__name__)


class ModuleUtils:
    @staticmethod
    def import_or_install(module: str, package: str, force_reinstall: bool):
        if force_reinstall:
            pip.main(['install', package, "--force-reinstall"])
            return
        try:
            __import__(module)
        except ImportError:
            pip.main(['install', package])


class ResolverBase(ABC):
    def __init__(self, module_name, target: Any):
        self.module_name = module_name
        self.target = target

    @abstractmethod
    def create_context(self):
        pass

    @abstractmethod
    def module_callback(self, ctx, module_path: str, module):
        pass

    def resolve(self):
        ctx = self.create_context()
        main_module = importlib.import_module(self.module_name)
        try:
            cdsw_module_path = f"{self.module_name}.cdsw"
            cdsw_module = importlib.import_module(cdsw_module_path)
        except ModuleNotFoundError as e:
            raise CdswLauncherException(f"Cannot find cdsw module in module: {self.module_name}") from e

        self._traverse_modules(ctx, cdsw_module_path, cdsw_module, self.module_callback)
        app_type = ctx.check_result()
        return app_type

    @classmethod
    def _traverse_modules(cls, ctx, module_path, curr_module, callback):
        callback(ctx, module_path, curr_module)
        # https://docs.python.org/3/reference/import.html#:~:text=By%20definition%2C%20if%20a%20module,search%20for%20modules%20during%20import.
        is_package = hasattr(curr_module, "__path__")
        if is_package:
            for mod_info in pkgutil.iter_modules(curr_module.__path__):
                new_module_path = f"{module_path}.{mod_info.name}"
                new_module = importlib.import_module(new_module_path)
                cls._traverse_modules(ctx, new_module_path, new_module, callback)


class ClassResolverContext:
    def __init__(self, module_name: str, target: Any):
        self.module_name = module_name
        self.target = target
        self._found = {}
        self._traversed_modules = []

    def add_result(self, module_path, apps: Iterable[CdswApp]):
        if module_path in self._found:
            raise ValueError("Module path already added to found apps!")
        self._found[module_path] = apps

    def check_result(self):
        cname = CdswApp.__name__

        if not self._found.keys():
            raise ValueError(f"{cname} not found in module: {self.module_name}. Traversed modules: {self._traversed_modules}")
        if len(self._found.keys()) > 1:
            raise ValueError(f"Multiple {cname}s found: {self._found} in module: {self.module_name}.")

        mod_key = list(self._found.keys())[0]
        apps = self._found[mod_key]
        if len(apps) != 1:
            raise ValueError(f"Multiple {cname}s found in module: {mod_key}")

        return apps[0]

    def process_module(self, mname):
        LOG.debug("Processing module: %s", mname)
        self._traversed_modules.append(mname)


class ClassResolver(ResolverBase):
    def __init__(self, module_name, target: Any):
        super().__init__(module_name, target)

    def create_context(self):
        return ClassResolverContext(self.module_name, self.target)

    def module_callback(self, ctx, module_path: str, module):
        ctx.process_module(module.__name__)

        apps: List[CdswApp] = []
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isclass(attribute) and issubclass(attribute, ctx.target):
                if "cdswjoblauncher" in attribute.__module__:
                    LOG.warning("Ignoring attribute: %s", attribute)
                else:
                    apps.append(attribute)

        if apps:
            ctx.add_result(module_path, apps)