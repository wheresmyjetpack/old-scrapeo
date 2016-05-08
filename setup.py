from setuptools import setup

setup(
    name='Scrap-EO',
    version= '1.0',
    py_modules=['scrapeo'],
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4',
        ],
    entry_points='''
        [console_scripts]
        scrapeo=scrapeo:cli
    ''',
)

