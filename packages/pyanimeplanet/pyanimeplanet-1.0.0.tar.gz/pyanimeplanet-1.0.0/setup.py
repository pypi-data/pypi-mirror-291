from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A python module to extract information from anime-planet website'
LONG_DESCRIPTION = 'A package that allows to extract information from anime planet website without login. This module uses the selenium web driver to scrap details from the web'

setup(
    name="pyanimeplanet",
    version=VERSION,
    author="Vishal Rashmika",
    author_email="<vishal.rashmika.perera@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['bs4', 'selenium==4.23.1'],
    keywords=['python', 'web-scraping', 'animeplanet', 'anime'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
    ]
)