from setuptools import setup
from os.path import abspath, dirname, join

README_MD = open(join(dirname(abspath(__file__)), 'README.md')).read()

setup(
    name = 'Visual-Phenomics-Py',
    version = '1.12.0',
    packages = ['visual_phenomics_py', 'visual_phenomics_py.util'],
    test_suite = 'tests',
    install_requires = ['numpy >= 1.21.5', 'pandas >= 1.3.5', 'matplotlib >= 3.5.1'],
    keywords = ['visual-phenomics', 'data-analysis', 'photosynthesis'],
    description='Import and reformat data output files from Visual Phenomics into a DataFrame.',
    long_description=README_MD,
    long_description_content_type='text/markdown',
    author='Sebastian Kuhlgert',
    author_email='sebastian.kuhlgert@gmail.com',
    url='https://github.com/SeBassTian23/Visual-Phenomics-Python',
    license='MIT'
)
