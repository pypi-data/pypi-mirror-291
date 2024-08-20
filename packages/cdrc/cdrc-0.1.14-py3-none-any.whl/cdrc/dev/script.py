import os
import subprocess
import sys
from pathlib import Path

PACKAGE = "cdrc"


def __getattr__(name):
    """
    HACK to make poetry execute shell scripts
    """
    print(f"fhslkdfjslkdf {name}")
    r = subprocess.run([f"./cdrc/scripts/{name}.sh"] + sys.argv[1:], env={**os.environ, "PACKAGE": PACKAGE})
    if r.returncode:
        sys.exit(r.returncode)
    return lambda: None


def run():
    args = sys.argv[1:]
    p = Path("../scripts")
    options = [f.stem for f in list(p.glob("*.sh"))]

    print(f"lskdfjs {options}")

    if next(iter(args), "") not in options:
        print("Invalid script option")  # noqa: T201
        print("Valid options:")  # noqa: T201
        print("\t" + "\n\t".join(options))  # noqa: T201
    else:
        r = subprocess.run([f"./scripts/{args[0]}.sh"] + sys.argv[1:], env={**os.environ, "PACKAGE": PACKAGE})

        sys.exit(r.returncode)
