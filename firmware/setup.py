from setuptools import setup

setup(
   name='firmware',
   version='0.2.0',
   author='ylpoonlg',
   author_email='poon.yat.long@gmail.com',
   packages=['firmware'],
   install_requires=[
       "numpy",
       "matplotlib",
       "pyserial"
   ],
)