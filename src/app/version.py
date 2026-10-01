import importlib.metadata
from functools import cache


@cache
def get_app_version():
    # current installed version in current env
    # for prod - package version (or poetry?)
    # for dev - poetry locked and installed version
    # package name from pyproject.toml
    try:
        return importlib.metadata.version("test-app")
    except importlib.metadata.PackageNotFoundError:
        return "<n/a>"
