from setuptools import setup, find_packages

setup(
    name='ratios_calculator',
    version='0.0.2',
    author='Bill Jiang',
    author_email='bcv0906@gmail.com',
    install_requires=[
        'pandas',
        'numpy',
        'dash == 2.17.1',
        'datetime',
        'openpyxl>=3.1.3'
    ],
    license="MIT",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    description='A package for calculating and analyzing financial ratios',
    long_description=open('app/README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/equate-fund/financial_ratios',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["twine>=4.0.2"]
    },
    python_requires='>=3.6',
)
