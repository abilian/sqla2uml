import importlib
import inspect
import pkgutil
from dataclasses import dataclass
from pathlib import Path

from devtools import debug
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute


@dataclass(frozen=True)
class ClassInfo:
    cls: type

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.cls == other.cls

    @property
    def __name__(self):
        return self.cls.__name__

    @property
    def __bases__(self):
        return self.parents

    @property
    def parents(self) -> list:
        return [ClassInfo(parent) for parent in self.cls.__bases__]

    @property
    def properties(self) -> list:
        result = []
        for k, v in vars(self.cls).items():
            if isinstance(v, InstrumentedAttribute):
                result.append(k)
        return result

    @property
    def own_properties(self) -> list:
        result = []
        base_classes = self.parents
        for prop in self.properties:
            if any(prop in base.properties for base in base_classes):
                continue
            result.append(prop)
        return result


class Scanner:
    def __init__(self, debug_level=0):
        self.models = set()
        self.debug_level = debug_level

    def scan(self, module) -> set:
        module_name = module.__name__
        self.import_all(module)

        result = set()
        for obj in list(vars(module).values()):
            if inspect.ismodule(obj):
                if not obj.__name__.startswith(module_name):
                    continue
                result |= self.scan(obj)
                continue

            if not inspect.isclass(obj):
                continue

            if obj.__module__ != module.__name__:
                continue

            if self.debug_level:
                debug(type(obj))
            if issubclass(type(obj), DeclarativeMeta):
                result.add(ClassInfo(obj))

        return result

    def import_all(self, module):
        path = str(Path(module.__file__).parent)
        module_name = str(module.__name__)

        for finder, name, ispkg in pkgutil.walk_packages([path]):
            fqname = module_name + "." + name
            # debug(finder, module_name, name, ispkg, fqname)
            try:
                importlib.import_module(fqname)
            except:
                # FIXME: ignore all errors for now, this needs to be fixed
                # because this will confuse users
                pass
            # except ModuleNotFoundError:
            #    pass
