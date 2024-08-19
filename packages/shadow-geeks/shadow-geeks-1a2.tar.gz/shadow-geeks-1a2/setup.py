from setuptools import setup, find_packages

setup(
    name='shadow-geeks',
    version='1.a.2',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pyzipper",
    ],
    package_data={
        'shadow_geeks': ['*.rar'],
    },
    description='A package created for team shadow geeks',
    long_description="Created by Rahul. This module contains required items for shadow geeks to build and run their projects anywhere",
    long_description_content_type='text/markdown',
    author='Rahul',
    author_email='rockr3876@gmail.com',
    license='MIT',
)