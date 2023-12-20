from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Vadym Zelenin'

requirements = [
    'selenium==2.53.6',
    'clarifai==2.0.32',
    'pyvirtualdisplay',
    'emoji'
]

description = 'Instagram Like, Comment and Follow Automation Script'

setup(
    name='instagram_py',
    version=__version__,
    author=__author__,
    author_email='wadedevelop@gmail.com',
    url='https://github.com/pewstiepoll/instagrambot',
    py_modules='instapy',
    description=description,
    install_requires=requirements,
    packages=['instagram_bot'],
    include_package_data=True,
)
