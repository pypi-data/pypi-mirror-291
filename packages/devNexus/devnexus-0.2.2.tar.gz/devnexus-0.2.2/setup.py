# setup.py
from setuptools import setup, find_packages

setup(
    name='devNexus',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'openai',
        'pyperclip',
        'requests',
        'bs4'
    ],
    include_package_data=True,
    description='A package containing dev tools to make development easier.',
    long_description=open('Readme.md').read(),
    long_description_content_type='text/markdown',
    author='PZ',
    author_email='rade.dvlp@gmail.com',
    url='https://github.com/2snufkin/developer_tools',  # Update with your GitHub repo link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7.1',
)
