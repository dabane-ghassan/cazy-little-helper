import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='cazy-little-helper',
    version='1.1.1',
    description='A biocuration assistant for the CAZy database.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dabane-ghassan/cazy-little-helper',
    author='dabane-ghassan',
    author_email = 'dabane.ghassan@gmail.com',
    download_url = 'https://github.com/dabane-ghassan/cazy-little-helper/archive/refs/tags/v1.1.1tar.gz',
    license='MIT',
    packages=setuptools.find_packages(include=['cazy_little_helper', 'cazy_little_helper.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    extras_require={
        'dev': [
            'pytest >= 6.0.0',
            'pytest-cov >= 2.10.0',
            'coveralls >= 2.1.2',
            'flake8 >= 3.8.0',
            'mock >= 4.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'predict=cazy_little_helper.predict:main',
            'create=cazy_little_helper.create_model:main',
            'find=cazy_little_helper.find_ids:main',
        ]
    },
    python_requires='>=3.6',
)
