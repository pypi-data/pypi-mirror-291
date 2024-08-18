from setuptools import setup, find_packages

setup(
    name='genkit',
    version='0.2.0',
    description='A Python package for generating random data like phone numbers .',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Suhail Shaji',
    author_email='suhailshaji@gmail.com',
    packages=find_packages(include=['genkit', 'genkit.*']),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='random phone number generator, genkit, generate random phone number with country code',
)