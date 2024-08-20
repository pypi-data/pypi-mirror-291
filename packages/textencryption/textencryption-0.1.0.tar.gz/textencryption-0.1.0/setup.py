from setuptools import setup, find_packages

setup(
    name='textencryption',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple text and file encryption tool using Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/textencryption',  # Update with your repo URL
    packages=find_packages(),
    install_requires=[
        'cryptography>=3.4.7',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'textencrypt=encryption_package.userinterface:main',
        ],
    },
)
