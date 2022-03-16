import importlib

import click
from devtools import debug

from sqla2uml.generator import Generator
from sqla2uml.scanner import Scanner

DEFAULT_CONFIG = {
    "root-dir": ".",
    "root-module": ".",
}


@click.command()
@click.option("--module", "-m", default=".", help="Package to analyse (recursively)")
@click.option(
    "--output", "-o", default="-", help="File to output result (defaults to stdout)"
)
@click.option(
    "--properties", "-p", is_flag=True, help="Include properties in diagrams"
)
@click.option(
    "--exclude", "-x", default="", help="List of class names to exclude from diagram"
)
@click.option("--debug-level", "-d", default=0, help="Debug level")
def main(module: str, exclude: str, output: str, properties, debug_level: int):
    config = DEFAULT_CONFIG

    scanner = Scanner()
    root_module = importlib.import_module(module)
    models = scanner.scan(root_module)

    if debug_level:
        debug(models)

    config["exclude"] = exclude
    config["properties"] = properties

    generator = Generator(models, config=config)
    output_fd = click.open_file(output, "w")
    generator.generate(output_fd)


if __name__ == "__main__":
    main()
