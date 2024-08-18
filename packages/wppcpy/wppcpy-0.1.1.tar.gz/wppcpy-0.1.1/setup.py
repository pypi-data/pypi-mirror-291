from setuptools import setup, find_packages

setup(
    name='wppcpy',
    version='0.1.1',
    url='https://github.com/shahmal1yev',
    license='MIT',
    author='shahmal1yev',
    description='Verify that the directory is a WordPress plugin based on the defined constraints.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages()
)
