from setuptools import setup, find_packages

setup(
    name='corerec',
    version='0.1.0',
    description='Graph-based recommendation systems using neural network architectures.',
    author='Vishesh',
    author_email='your-email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy',  # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)