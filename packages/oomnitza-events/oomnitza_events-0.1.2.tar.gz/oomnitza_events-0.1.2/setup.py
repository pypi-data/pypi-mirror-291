import setuptools

from oomnitza_events import version

requirements = [
    "analytics-python==1.2.9",
    "arrow",
    "Cerberus",
    "psycopg2-binary==2.9.9",
    "typing_extensions",
]

dev_requirements = [
    "pytest",
    "pytest-pep8",
    "pytest-cov",
    "wheel",
]

setuptools.setup(
    name="oomnitza-events",
    version=version.__version__,
    packages=setuptools.find_packages(exclude=["tests"]),
    description="This project is developed for tracking Oomnitza activities.",
    long_description="This project is developed for tracking Oomnitza activities.",
    author="Oomnitza",
    author_email="etl-admin@oomnitza.com",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
)
