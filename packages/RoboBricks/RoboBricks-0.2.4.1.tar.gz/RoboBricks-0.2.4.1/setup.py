from setuptools import setup
from RoboBricks.constants_lib import RoboBricksConst

with open("README.md", "r") as fh:
    ld = fh.read()

setup(
      name              =RoboBricksConst.library_name,
      version           =RoboBricksConst.library_version,
      description       =RoboBricksConst.library_description,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
      ],
      keywords          =RoboBricksConst.library_name,
      url               =RoboBricksConst.library_url,
      author            =RoboBricksConst.library_author,
      author_email      =RoboBricksConst.library_author_email,
      packages          =['RoboBricks'],
      zip_safe          =False,
      long_description  =ld,
      long_description_content_type="text/markdown",
      python_requires   ='>=3.8',
      )