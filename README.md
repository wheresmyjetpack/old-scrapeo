# scrap-eo
CLI for scraping data from webpages for SEO analysis

## Installation
It is recommended that you have the *virtualenv* Python package installed so scrap-eo can install it's required packages in an isolated environment without risk of creating conflicts with existing Python packages already installed on your system.

`pip install virtualenv`

You may have to run the above command as root.
With virtualenv installed on your system, you can follow the recommended steps below to install scrap-eo in its own isolated environment:

* clone the scrap-eo repo
* `mkdir -p ~/.virtualenvs`
* `virtualenv ~/.virtualenvs/scrapeo`
* `source ~/.virtualenvs/scrapeo/bin/activate`
* `cd` into the cloned repo
* `pip install .`
* `deactivate`

After running `pip install .`, an executable Python file will be generated in your *.virtualenvs/scrapeo/bin* directory called *scrapeo*. It is useful to create a symbolic link to this file in a directory that is listed for your path. For example `ln -s /home/<user>/.virtualenvs/scrapeo/bin/scrapeo /usr/local/bin/scrapeo` will allow you to run scrapeo from anywhere without having to type the full path to the executable (if */usr/local/bin/* is listed in your path environment variable).

Alternatively, if you want to contribute to scrap-eo, it is recommended that you `pip install --editable .` so any changes you make to the source code take effect immediately. Otherwise, you must reinstall scrap-eo everytime you make changes.

## Planned Features
* Create an API for scrap-eo, moving the functions for scraping data to a separate file that contains a `ScrapEO` class 
* Add an argument to the `--meta` option to scrape the content from all meta tags in a document (e.g. `--meta *`)
* Add regex matching functionality to the `--meta` option
* Add option to audit sites making use of HTML5 spec 
* Add colored output support ([colorama](https://pypi.python.org/pypi/colorama) integration with click)
