from setuptools import setup, find_packages

setup(
    name='alex_random_dice',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies your library needs
    author='Alexander Hughes',
    author_email='alexanderisaachughes@googlemail.com',
    description='A simple example Python library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
