"""Main module."""

import importlib
import inspect
from dataclasses import dataclass

from sqlalchemy.orm import InstrumentedAttribute

BLACKLIST = {
    "Model",
    "IdMixin",
    "LifeCycleMixin",
    "Owned",
    "UserFeedbackMixin",
}


@dataclass
class Class:
    cls: type

    @property
    def base_classes(self) -> list:
        return [Class(parent) for parent in self.cls.__bases__]

    @property
    def properties(self) -> list:
        result = []
        for k, v in inspect.getmembers(self.cls):
            if isinstance(v, InstrumentedAttribute):
                result.append(k)
        return result

    @property
    def own_properties(self) -> list:
        result = []
        base_classes = self.base_classes
        for prop in self.properties:
            if any(prop in base.properties for base in base_classes):
                continue
            result.append(prop)
        return result


def gather_models(module) -> set:
    result = set()
    for obj in vars(module).values():
        if inspect.ismodule(obj):
            if not obj.__name__.startswith(module.__name__):
                continue
            result |= gather_models(obj)
            continue

        if (
            inspect.isclass(obj)
            and issubclass(obj, db.Model)
            and obj.__module__ == module.__name__
        ):
            # debug(vars(obj))
            result.add(obj)

    return result


def generate_uml(path_or_module):
    if isinstance(path_or_module, str):
        module = importlib.import_module(path_or_module)
    else:
        module = path_or_module

    models = gather_models(module)
    models = {m for m in models if m.__name__ not in BLACKLIST}

    with open("doc/model-simple.puml", "w") as fd:
        generate_puml(models, fd)

    with open("doc/model-detailed.puml", "w") as fd:
        generate_puml(models, fd, detailed=True)


# def generate_fields(model):
#     cls = Class(model)
#     lines = []
#     for prop in cls.own_properties:
#         lines += [f"  +{prop}"]
#     return "\n".join(lines)


def generate_puml(models, fd, detailed=False):
    output = fd
    output.write("@startuml\n")

    for model in models:
        if detailed:
            cls = Class(model)
            fields = cls.own_properties
        else:
            fields = []

        output.write(f"class {model.__name__} {{\n")
        for field in fields:
            output.write(f"  +{field}\n")
        output.write("}\n")

    output.write("\n")

    for model in models:
        for parent in model.__bases__:
            if parent.__name__ in BLACKLIST:
                continue
            output.write(f"{model.__name__} -up-|> {parent.__name__}\n")

    output.write("\n")
    output.write("@enduml\n")


def main():
    import app.models

    _app = create_app()

    # Scan the apps register all models
    scanner = venusian.Scanner()
    scanner.scan(app.models)

    with _app.app_context():
        generate_uml("app.models")


if __name__ == "__main__":
    main()
