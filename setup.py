from setuptools import setup
import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as requirements_file:
    requirements = requirements_file.readlines()
    install_requires = [req for req in requirements if not req.startswith('http')]

main_ns = {}
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version.py')) as ver_file:
    exec(ver_file.read(), main_ns)

setup(name='cda.pl.downloader',
      version=main_ns['__version__'],
      description='Download videos from cda.pl',
      author='s4980',
      author_email='s4980@github.com',
      packages=['cdapldownloader'],
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['cda.pl-downloader=cdapldownloader.command_line:main'],
      },
      include_package_data=True,
      zip_safe=True)
