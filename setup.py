from setuptools import setup, find_packages

setup(
    name='Scrap-EO',
    version= '1.1.2',
    packages = find_packages(),
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4',
        'colorama'
        ],
    entry_points='''
        [console_scripts]
        scrapeo=main:cli
    ''',
)

