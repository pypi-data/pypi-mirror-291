from setuptools import setup, find_packages

setup(
    name='apiverve_moonrisemoonset',
    version='1.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Moonrise Moonset is a simple tool for getting moonrise and moonset times. It returns the moonrise and moonset times based on the location provided.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
