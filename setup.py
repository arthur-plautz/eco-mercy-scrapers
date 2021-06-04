from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ecscrapers",
    version="0.1.0",
    author="Arthur Plautz Ventura",
    author_email="atr.plautz@gmail.com",
    description="Scrapers for E-Commerce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arthur-plautz/eco-mercy-scrapers",
    project_urls={
        "Bug Tracker": "https://github.com/arthur-plautz/eco-mercy-scrapers/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"ecscrapers": "ecscrapers"},
    package_data={"ecscrapers": ['config/*/*']},
    include_package_data=True,
    packages=find_packages(include=['ecscrapers', 'ecscrapers.*']),
    python_requires=">=3.7",
    install_requires=[
        'cycler==0.10.0',
        'kiwisolver==1.3.1',
        'numpy==1.20.3',
        'pandas==1.2.4',
        'Pillow==8.2.0',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'pytz==2021.1',
        'PyYAML==5.4.1',
        'selenium==3.141.0',
        'six==1.16.0',
        'urllib3==1.26.5'
    ]
)