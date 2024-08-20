from setuptools import setup, find_packages


setup(
    name='django-ministripe',
    version='0.0.1',
    packages=find_packages(),
    description='A tiny Django package for managing Stripe subscriptions',
    url='https://github.com/kennell/django-ministripe',
    author='Kevin Kennell',
    author_email='kevin@kennell.de',
    install_requires=[
        'django',
        'stripe'
    ]
)
