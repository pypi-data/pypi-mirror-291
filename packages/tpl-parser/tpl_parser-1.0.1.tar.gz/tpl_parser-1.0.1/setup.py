from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tpl-parser',
    version='1.0.1',
    author='Dev Jones',
    author_email='devjonescodes@gmail.com',
    description='A Python package to parse Photoshop TPL files and extract data into JSON format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DavyJonesCodes/TPLParserPy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'tpl-parser=TPLParser.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license_files=['LICENSE'],
)
