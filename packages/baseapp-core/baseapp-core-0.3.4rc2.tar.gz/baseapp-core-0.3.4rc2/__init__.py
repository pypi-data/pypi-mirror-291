from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("package-name")
except PackageNotFoundError:
    # TODO: temporary fix to our circular dependency in development and CI/CD environments
    # we should either fix the circular dependency OR use pypi versions instead of local/development ones under CI/CD
    __version__ = "0.3.3"
