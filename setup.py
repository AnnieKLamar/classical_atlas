
from distutils.core import setup
setup(
  name = 'classical_atlas',         # How you named your package folder (MyLib)
  packages = ['classical_atlas'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python package for accessing open-source geospatial datasets.',   # Give a short description about your library
  author = 'Annie K. Lamar',                   # Type in your name
  author_email = 'kalamar@stanford.edu',      # Type in your E-Mail
  url = 'https://github.com/AnnieKLamar/classical_atlas',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AnnieKLamar/classical_atlas/archive/refs/tags/v1.13.tar.gz',
  keywords = ['Pleiades', 'network', 'geospatial', 'open access', 'digital humanities', 'archaeology'],   # Keywords that define your package best
  install_requires=[
          'collections',
          'networkx',
          'json',
          'os',
          'beautifulsoup4',
          'csv'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      #Specify which Python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)