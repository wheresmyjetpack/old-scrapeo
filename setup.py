from setuptools import setup

setup(
    name='Scrap-EO',
    version= '1.0',
    packages = find_packages(),
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4',
        ],
    entry_points='''
        [console_scripts]
        scrapeo=main:cli
    ''',
)

