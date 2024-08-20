from setuptools import setup

setup(
    name='database_setup',
    version='0.1.2',
    description='Database setup utilities with configuration handling',
    author='Komal',
    author_email='komal@neudeep.in',
    packages=['database_setup'],
    install_requires=[
        'pymysql',
        'dbutils',
        'PyYAML',
    ],
)