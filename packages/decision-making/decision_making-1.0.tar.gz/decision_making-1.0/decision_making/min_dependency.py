# All minimum dependencies for decsion-making
NUMPY_MIN_VERSION = "1.26.4"
SCIPY_MIN_VERSION = "1.13.0"
PANDA_MIN_VERSION = "2.2.2"


MIN_DEPENDENCIES = {
    "numpy": NUMPY_MIN_VERSION,
    "scipy": SCIPY_MIN_VERSION,
    "pandas": PANDA_MIN_VERSION
}

#list of required dependencies
install_requires = [f"{pkg}>={version}" for pkg, version in MIN_DEPENDENCIES.items()]
