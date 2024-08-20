from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='starecase-cron-monitor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author='Aman Madhukar',
    author_email='madhukaraman02@gmail.com  ',
    description='This is a Python package designed for monitoring cron jobs through Starecase.io',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/madhukaraman/starecase-cron-monitor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
