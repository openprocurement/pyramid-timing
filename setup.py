from setuptools import setup, find_packages
import os

version = '0.1dev'

test_requires = [
    'mock',
    'nose',
    'python-coveralls',
    'coverage'
]

requires = [
    'setuptools',
    'pyramid',
] + test_requires

entry_points = {
    'openprocurement.api.plugins': [
        'pyramid_timing = pyramidtiming.tween:includeme'
    ]
}

setup(name='pyramidtiming',
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
      namespace_packages=['pyramidtiming'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points=entry_points
      )
