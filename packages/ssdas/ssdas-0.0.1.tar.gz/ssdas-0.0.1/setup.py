from setuptools import setup, find_packages

setup(
    name='ssdas',
    version='0.0.1',
    description='smart and speedy data analysis and statistics',
    author='StarryNight82',
    author_email='rie82sm@naver.com',
    url='https://github.com/StarryNight82/ssdas',
    install_requires=['numpy', 'pandas',],
    packages=find_packages(exclude=[]),
    keywords=['StarryNight82', 'financial data handling', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)