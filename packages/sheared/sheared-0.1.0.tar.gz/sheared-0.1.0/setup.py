from setuptools import setup, find_packages

setup(
    name='sheared',  # Name of your library
    version='0.1.0',  # Initial version number
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[],  # List of dependencies
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your library',
    url='https://github.com/yourusername/sheared',  # URL of the library's repository or website
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python versions your library supports
)
