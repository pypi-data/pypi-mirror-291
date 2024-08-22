from setuptools import setup, find_packages

setup(
    name='codeforcess',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'codeforces-fetch=codeforcess.downloader:fetch_all_problems',
        ],
    },
    author='Sudhir Sharma',
    author_email='sudhirsharma@iitbhilai.ac.in',
    description='A package to download all Codeforces problems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sudhir878786/codeforces-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
