from setuptools import setup, find_packages

# exclude server directory
# exclude test files
setup(
    name='irpkgca1',
    version='0.0.7',
    url='https://github.com/vsaravind01/ir_pkg',
    maintainer='Senapathy Veerasekaran',
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent", ],
    description='description',
    keywords=[],
    packages=find_packages(),
    project_urls={},
    python_requires='>=3.7')
