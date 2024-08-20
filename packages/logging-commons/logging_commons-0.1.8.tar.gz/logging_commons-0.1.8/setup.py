from setuptools import setup, find_packages

setup(
    name="logging-commons",
    version="0.1.8",
    url="https://github.com/KaribuLab/python-logging-commons",
    long_description_content_type = "text/markdown",
    license="Apache Software License",
    author="Patricio Ascencio",
    author_email="paascencio@gmail.com",
    description="Python Logging Tools",
    python_requires=">=3.12",
    packages=find_packages(),
    include_package_data=True,
    platforms=["MacOS X", "Linux", "Windows"],
)
