from setuptools import setup, find_packages
import os

version = '0.1dev'

requires = [
    'setuptools',
    'pyramid',
]

entry_points = {
    'openprocurement.api.plugins': [
        'timing_tween = timingtween.timingtween.tween:includeme'
    ]
}

setup(name='timingtween',
      version=version,
      description="",
      long_description=open("README.md").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      url='',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['timingtween'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points=entry_points
      )
