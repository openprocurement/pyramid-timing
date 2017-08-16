from setuptools import setup, find_packages
import os

version = '1.0'

test_requires = [
    'mock',
    'nose',
    'flask-testing',
    'python-coveralls',
    'webtest',
]

requires = [
    'setuptools',
    'webob',
]

extras_require = {
    'pyramid': ['pyramid',] + requires,
    'flask': ['flask',] + requires,
    'test': test_requires + requires
}

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
      extras_require=extras_require,
      entry_points=entry_points
      )
