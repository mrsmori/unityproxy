from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='UnityProxy',
      version='0.0.2',
      description='Proxy parser and converter',
      author='Lisica',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email='nomail@google.com',
      url='https://github.com/mrsmori/unityproxy',
      
      packages=find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
     )