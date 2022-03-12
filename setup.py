from setuptools import setup
from os.path import abspath, dirname, join

README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()

setup(
    name = "Visual-Phenomics-Py",
    version = "1.2.0",
    packages = ['visual_phenomics_py'],
    test_suite = 'tests',
    install_requires = ['numpy', 'pandas', 'matplotlib'],
    keywords = ['visual-phenomics', 'text-analysis', 'etymology'],
    description='Import and reformat data output files from Visual Phenomics into a DataFrame.',
    long_description=README_MD,
    long_description_content_type="text/markdown",
    author='Sebastian Kuhlgert',
    author_email='sebastian.kuhlgert@gmail.com',
    url='https://github.com/SeBassTian23/Visual-Phenomics-Python',
    license='MIT'
)
