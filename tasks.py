import re
from pathlib import Path

from invoke import Context, task


@task()
def help(c: Context):
    c.run("invoke --list")


@task()
def help_make(c: Context):
    """Helper to generate the `make help` message"""
    with Path(__file__).parent.joinpath("Makefile").open() as f:
        makefile = f.read()

    description = ""
    targets = []
    for line in makefile.splitlines():
        if m := re.match(r"^## (.*)", line):
            description = m.group(1)
        elif m := re.match("^(.*?):", line):
            target = m.group(1)
            if description:
                targets.append([target, description])
        else:
            description = ""

    if not targets:
        print("No targets found")
        return

    print("Targets:\n")
    max_len = max(len(t[0]) for t in targets)
    for targets, description in targets:
        print(f"{targets:<{max_len}}  {description}")
