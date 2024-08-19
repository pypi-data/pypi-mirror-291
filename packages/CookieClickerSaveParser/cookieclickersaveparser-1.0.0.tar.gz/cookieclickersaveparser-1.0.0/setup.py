import re
from setuptools import setup, find_packages


def __get_version():
    with open("CCParse/__init__.py") as package_init_file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', package_init_file.read(), re.MULTILINE).group(1)


requirements = []

setup(
    name='CookieClickerSaveParser',
    version=__get_version(),
    url='https://github.com/Tevtongermany/CookieClickerSaveConverter',
    license='Mozilla Public License Version 2.0',
    author='Tevtongermany',
    author_email='Tevtongermany@femboy.cx',
    description='Basic Cookie Clicker Save parser',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)