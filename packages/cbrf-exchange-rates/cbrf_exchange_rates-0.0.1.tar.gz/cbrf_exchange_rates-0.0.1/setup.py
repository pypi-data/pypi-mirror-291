from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='cbrf_exchange_rates',
    version="0.0.1",
    description='Client for The Central Bank of the Russian Federation APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cooper30/cbrf_exchange_rates.git',
    license='MIT',
    author='Nikita Zvekov',
    author_email='cooper30@mail.ru',
    install_requires=['requests'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires="~=3.12",
)
