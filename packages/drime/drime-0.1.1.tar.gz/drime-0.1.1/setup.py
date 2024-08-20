from setuptools import setup, find_packages

setup(
    name='drime',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='PainDe0Mie',
    author_email='painde0mie@example.com',
    description='A Python package for interacting with the Drime API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PainDe0Mie/drime',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)