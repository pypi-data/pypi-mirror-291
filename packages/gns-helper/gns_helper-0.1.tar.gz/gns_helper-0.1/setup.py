# setup.py
from setuptools import setup, find_packages

setup(
    name='gns_helper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-JWT-Extended',
        'Pillow',
        'pymysql',
        # Add other dependencies here
    ],
    include_package_data=True,
    description='A package for common GNS functions',
    author='Komal Swami',
    author_email='komalsswami@gmail.com',
    #url='https://github.com/yourusername/gns_helpers',  # Optional
)