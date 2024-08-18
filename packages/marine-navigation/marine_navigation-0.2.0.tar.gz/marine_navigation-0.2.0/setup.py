from setuptools import setup, find_packages

setup(
    name='marine_navigation',
    version='0.2.0',
    description='A package to calculate tidal windows for marine vessels entering ports.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    include_package_data=True,
)

