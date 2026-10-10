from pathlib import Path
from setuptools import find_packages, setup


ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")


setup(
    name="idict-schema",
    version="1.0.0",
    author="Slawomir Hadas",
    author_email="slawekgithub1218@gmail.com",
    description="Extended defaultdict with declared structure and validation rules",
    license="GPL-3.0-only",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hadasbro/idict",
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.7",
    keywords=["dict", "defaultdict", "validation", "schema"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Source": "https://github.com/hadasbro/idict",
        "Issues": "https://github.com/hadasbro/idict/issues",
    },
)
