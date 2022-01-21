from devtools import debug

from sqla2uml.scanner import ClassInfo

EXCLUDED = set()


class Generator:
    def __init__(self, models, debug_level=0, config=None):
        assert all(isinstance(cls, ClassInfo) for cls in models)

        self.debug_level = debug_level

        # TODO
        self.models = {m for m in models if m.__name__ not in EXCLUDED}

        if config is None:
            self.config = {}
        else:
            self.config = config

    def generate(self, fd):
        detailed = self.config["properties"]
        self.generate_puml(fd, detailed)

    def generate_puml(self, fd, detailed=False):
        output = fd
        output.write("@startuml\n")

        for model in self.models:
            assert isinstance(model, ClassInfo)
            if detailed:
                fields = model.own_properties
            else:
                fields = []

            output.write(f"class {model.__name__} {{\n")
            for field in fields:
                output.write(f"  +{field}\n")
            output.write("}\n")

        output.write("\n")

        for model in self.models:
            for parent in model.__bases__:
                if parent.__name__ in EXCLUDED:
                    continue
                output.write(f"{model.__name__} -up-|> {parent.__name__}\n")

        output.write("\n")
        output.write("@enduml\n")
