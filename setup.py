from distutils.core import setup

setup(
    name='ForecastCards',
    version='0.1.0dev',
    packages=['forecastcards'],
    install_requires=['pandas==0.22',
                      'requests',
                      'goodtables',
                      'tableschema',
                      'graphviz',
                      'statsmodels'],
    package_data={'forecastcards': ['examples/*']},
    long_description=open('README.txt').read(),
)