from setuptools import setup, find_packages

setup(
    name="Webstore_Scraper_PY",
    version="0.2.19",
    description="A Python library for scraping data from Goodwill and Ebay.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Scottyboi1/Webstore_Scraper",
    author="Scott Avery",
    author_email="scottavery2001@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
