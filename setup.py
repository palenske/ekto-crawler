from setuptools import setup

setup(
    name="ekto-crawler",
    description="Tool to filter results from a scraping made on an electronic music site: https://ektoplazm.com/",
    install_requires=[
        "parsel==1.6.0",
        "requests==2.27.1",
        "pymongo==4.1.1",
    ],
    setup_requires=["pytest-runner"],
    testes_require=["pytest"],
)
