from os import path

from setuptools import find_packages, setup

requires = [
    "PyHamcrest>=2.0.0,<2.1",
    "allure-pytest>=2.8.0,<2.9",
    "selenium>=3.141.0,<4.1.0",
    "pyotp>=2.4.0,<2.5.0",
    "requests>=2.25.0,<2.26.0",
    "typing-extensions>=3.7.4,<3.8",
]

repo_dir = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(repo_dir, "screenpy", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
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
    scripts=["bin/screenpy-quickstart.py"],
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
