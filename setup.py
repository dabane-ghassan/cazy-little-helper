import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cazy-little-helper',
    version='0.1',
    description='A biocuration assistant for the CAZy database.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dabane-ghassan/cazy-little-helper',
    author='dabane-ghassan',
    author_email = 'dabane.ghassan@gmail.com',
    #download_url = 'https://github.com/dabane-ghassan/dnazip/archive/v0.2.tar.gz',
    license='MIT',
    packages=setuptools.find_packages(include=['cazy-little-helper', 'cazy-little-helper.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements.txt,
    extras_require={
        'dev': [
            'pytest >= 6.0.0',
            'pytest-cov >= 2.10.0',
            'coveralls >= 2.1.2',
            'flake8 >= 3.8.0',
            'mock >= 4.0.0',
        ]
    },
    #entry_points={
    #    'gui_scripts': [
    #        'dnazip=dnazip.main:main'
    #    ]
    #},
    python_requires='>=3.6',
)
