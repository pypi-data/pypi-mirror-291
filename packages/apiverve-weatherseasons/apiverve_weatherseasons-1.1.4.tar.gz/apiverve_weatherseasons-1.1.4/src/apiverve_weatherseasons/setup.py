from setuptools import setup, find_packages

setup(
    name='apiverve_weatherseasons',
    version='1.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Weather Seasons is a simple tool for getting the dates of the solstice and equinox. It returns the dates of the solstice and equinox for the current year.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
