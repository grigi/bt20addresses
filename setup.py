import os
from setuptools import setup, find_packages

# This is to disable the 'black magic' surrounding versioned repositories... Terrible!
from setuptools.command import sdist
del sdist.finders[:]

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='bt20',
    version = '0.1',
    description='Project for bt20',
    long_description=read('README'),
    author='Internet Solutions',
    author_email='si@is.co.za',
    url='',
    zip_safe = False,

    # Dependencies
    install_requires = [
        'django >=1.4, <1.5',
        'pygeocoder',
    ],
    dependency_links = [
	# For example, this project would be something like:
        # 'git+ssh://git@github.com/InternetSolutions/bt20.git@master#egg=bt20-0.1',
    ],

    # Packages
    packages = find_packages(),
    include_package_data = True
)

