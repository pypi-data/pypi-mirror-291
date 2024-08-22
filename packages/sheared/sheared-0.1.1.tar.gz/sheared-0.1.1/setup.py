from setuptools import setup, find_packages


with open('./requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sheared',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    author='Abdulmajeed Alhadhrami',
    author_email='Abdulmajeed@example.com',
    description='A brief description of your library',
    url='https://github.com/mjid13/sheared',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
