"""
Humans
------

Add humans to SQLAlchemy based webapps.

"""
from setuptools import setup, find_packages


setup(
    name='Humans',
    version='0.1a',
    url='https://github.com/jeanphix/Humans',
    license='mit',
    author='Jean-Philippe Serafin',
    author_email='serafinjp@gmail.com',
    description='Add humans to SQLAlchemy based webapps.',
    long_description=__doc__,
    data_files=[('', ['README.md'])],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'SQLAlchemy',
        'passlib',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
