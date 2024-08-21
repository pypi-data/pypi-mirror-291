from setuptools import setup, find_packages

setup(
    name='apiverve_routingnumberlookup',
    version='1.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Routing Number Lookup is a simple tool for looking up routing number information for USA Banks. It returns information such as the bank, location, and more based on the routing number provided.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
