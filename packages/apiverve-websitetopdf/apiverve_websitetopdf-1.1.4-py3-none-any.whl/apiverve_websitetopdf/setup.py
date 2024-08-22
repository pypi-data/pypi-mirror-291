from setuptools import setup, find_packages

setup(
    name='apiverve_websitetopdf',
    version='1.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Website to PDF is a simple tool for converting a website to PDF. It returns the PDF file generated from the website.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
