"""Install ScreenPy!"""

from os import path

from setuptools import find_packages, setup

requires = [
    "PyHamcrest>=2.0.0",
    "pydantic>=1.10.0"
]

extras_require = {
    "allure": ["screenpy_adapter_allure"],
    "appium": ["screenpy_appium"],
    "playwright": ["screenpy_playwright"],
    "pyotp": ["screenpy_pyotp"],
    "requests": ["screenpy_requests"],
    "selenium": ["screenpy_selenium"],
}

repo_dir = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(repo_dir, "screenpy", "__version__.py")) as f:
    exec(f.read(), about)

with open("README.md") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    package_data={"screenpy": ["py.typed"]},
    packages=find_packages(),
    install_requires=requires,
    extras_require=extras_require,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: BDD",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ],
)
