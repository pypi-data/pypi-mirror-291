from setuptools import setup, find_packages

setup(
    name='CSGT',
    version='1.0.3',
    author='Manav Gupta',
    author_email='manav26102002@gmail.com',
    description='A deep learning library for Self-Organizing Maps (SOM) with clustering and gradient optimization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MM21B038/CSGO',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.4',
        'matplotlib==3.7.2',
        'scipy==1.11.2',
    ],
    extras_require={
        'dev': [
            'jupyter',
            'ipython',
            'pytest',
            'flake8'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
