from setuptools import find_packages, setup

with open('./README.md', 'r', encoding='utf-8') as fh:
  readme = fh.read()

setup(
  name='process_assistant',
  version='0.0.102',
  description='',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Pedro Jesús Pérez Hernández',
  author_email='pedrojesus.perez@welldex.mx',
  url='https://gitwell.gwldx.com:2443/python_libraries/envOS.git',
  install_requires=[],
  license='MIT',
  packages=find_packages(),
  include_package_data=True,
  entry_points={ 
        'console_scripts': [
            'testlib = process_assistant.process_assistant.main:main' 
        ]
    }
)