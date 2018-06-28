import os
import re

from setuptools import setup, find_packages

requires = [
    'Scrapy>=1.4',
    'requests>=2.18.4',
    'pymongo>=3.6.1'
]

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(os.path.join(ROOT, 'gs1-crawler'), '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='gs1-crawler',
    version=get_version(),
    description='gs1 information crawler',
    long_description=open('README.rst').read(),
    author='Bluehack',
    author_email='devops@bluehack.net',
    # url='https://github.com/BlueLens/gs1-crawler',
    scripts=[],
    package_data={
        # 'goodlens_crawler': [
        #     'data/*/*.csv',
        # ]
    },
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 1 - Planning',
    ],
)