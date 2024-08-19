from os import path as os_path

import setuptools

PACKAGE_NAME = "pyzf"
AUTHOR_NAME = "Zeff Muks"
AUTHOR_EMAIL = "zeffmuks@gmail.com"

with open("README.md", "r") as f:
    readme = f.read()


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), PACKAGE_NAME, "version.py")
    with open(version_file) as file:
        exec(file.read())
    version = locals()["__version__"]
    print(f"Building {PACKAGE_NAME} v{version}")
    return version


setuptools.setup(
    name=PACKAGE_NAME,
    version=read_version(),
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="pyzf is Zeff Muks's enhancement for working with Python",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt").read().splitlines(),
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"pyzf": ["pyzf/*.py"]},
    exclude_package_data={"": ["*.pyc", "*.pyo", "*.pyd", "__pycache__", "*.so", ".DS_Store"]},
)
