from setuptools import setup, find_packages

setup(name='datacrypt',
      version='0.1.6',
      description='datacrypt Package',
      packages=find_packages(),
      install_requires=["utilum", "fastapi", "jinja2", "markdown"],
      zip_safe=False,
      package_data={'': ['license.txt',
                         'web/templates/*.*',
                         'web/static/*.*',
                         'web/static/css/*.*', 'web/static/js/*.*']},
      include_package_data=True,
      )
