from setuptools import setup, find_packages

setup(
    name='photonix',  # Name of your package on PyPI
    version='0.1.0',  # Initial version
    description='A brief description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_project',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},  # Point to the src directory
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
