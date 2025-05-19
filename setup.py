from setuptools import find_packages, setup

setup(
    name="dagster_pipelines",
    packages=find_packages(exclude=["dagster_pipelines_tests"]),
    install_requires=[
        "dagster",
        "dagster-webserver",
        "requests",
        "pydantic",
        "SQLAlchemy",
        "psycopg2",
    ],
    extras_require={"dev": ["pytest"]},
)