from setuptools import setup, find_packages

setup(
  name='marine_navigation',
  version='0.3.0',
  description='A package to calculate tidal windows for marine vessels entering ports.',
  author='Your Name',
  author_email='your.email@example.com',
  packages=find_packages(),
  install_requires=[
      'csv',
      'pandas',
      'numpy',
      'scipy',
      'matplotlib',
  ],
  include_package_data=True,
  package_data={
    'marine_navigator': ['data/tide_heights.csv', 'data/ports.csv', 'data/vessels.csv'],
  },
)

