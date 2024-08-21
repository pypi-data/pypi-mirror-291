from setuptools import setup, find_packages
setup(
    name='pkcegen',
    version='1.0.1',
    description='A flexible and customizable PKCE generator for OAuth2 authentication.',
    author='70L0-0j0',
    author_email='70L0-0j0@lamia.xyz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/70L0-0j0/pkcegen',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)