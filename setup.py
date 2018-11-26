from distutils.core import setup

setup(
    name='ForecastCards',
    version='0.1.0dev',
    packages=['forecastcards'],
    package_dir   = { 'forecastcards':'forecastcards' },
    install_requires=['pandas==0.22',
                      'requests',
                      'goodtables',
                      'tableschema',
                      'graphviz',
                      'statsmodels'],
    package_data={'forecastcards': ['examples/*']},
)