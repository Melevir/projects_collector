# Project Collector

Simple script that clones Github projects, that matches search criteria.
Useful if you need to test your libraries on other code bases. 


## Requirements and installation

Python 3.6+, `git clone`, `pip install -r requirements.txt`.


## Usage
    
Usage: `python collect.py <script arguments>`.
Run `python collect.py --help` to see all arguments.

Simplest way to create search query is via [Github advanced search](https://github.com/search/advanced).


## Example

Download 2 python projects with 100+ stars sorted most forks amount:

    python collect.py --projects_amount=2 --sort_by=forks "stars:>100 language:Python"
