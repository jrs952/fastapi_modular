# setup.py

from setuptools import setup, find_packages

setup(
    name="fastapi.quickstart",
    version="1.0.0",
    description="A FastAPI application with plugin and service support.",
    author="Jared Szymurski",
    author_email="jared@szymurski.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "PyYAML",
        "httpx",
        "openai"
        # Include other dependencies as needed
    ],
    python_requires=">=3.8",
)
