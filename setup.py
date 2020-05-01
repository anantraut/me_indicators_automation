from setuptools import setup

setup(
    name='me_indicators_automation',
    packages=['me_indicators_automation'],
    include_package_data=True,
    install_requires=[
        'flask>=1.1.1',
        'pandas>=1.0.1',
        'xlrd >= 1.0.0'
    ],
)
