from setuptools import setup, find_packages

setup(
    name='apiverve_swiftcodelookup',
    version='1.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='SWIFT Code Lookup is a simple tool for looking up SWIFT code information. It returns information such as the bank, branch, and more based on the SWIFT code provided.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
