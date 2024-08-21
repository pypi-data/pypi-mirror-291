from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'A python module to extract information from anime-planet website'
LONG_DESCRIPTION = 'A package that allows to extract information from anime planet website without logging.'

setup(
    name="pyanimeplanet",
    version=VERSION,
    author="Vishal Rashmika",
    author_email="<vishal.rashmika.perera@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests==2.32.3', 'bs4'],
    keywords=['python', 'web-scraping', 'animeplanet', 'anime'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
    ]
)