from setuptools import setup, find_packages
setup(
    name='LicenceLibrary',
    version='0.1.0',
    author='StNiosem',
    author_email='bauch.aristide@gmail.com',
    description='A library for validating packages.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)