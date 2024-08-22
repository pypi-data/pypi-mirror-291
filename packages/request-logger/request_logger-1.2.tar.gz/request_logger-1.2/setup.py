from setuptools import setup, find_packages

setup(
    name='request_logger',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.rst'],
        'request_logger': ['middleware/*.py'],
    },
    install_requires=[
    ],
    author='Emre Türkmen',
    author_email='emre@parsyazilim.com',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EmreTurkmen-Hub/request-logger',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
