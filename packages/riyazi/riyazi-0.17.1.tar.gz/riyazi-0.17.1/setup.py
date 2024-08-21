from setuptools import setup


with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt") as reqs:
    requirements = reqs.read().split("\n") 
    
setup(
name='riyazi',
version = '0.17.1',
author = "Md Slauddin",
author_email="mdslauddin285@gmail.com",
license="MIT",
description="riyazi is a mathematics library",
long_description=LONG_DESCRIPTION,
long_description_content_type= 'text/x-rst', 
keywords=["Advance Math", "Math", "Engineering Math"],
url =  "https:github.com/Mdslauddin/riyazi-main",
# download_url = github zip link
install_requires = requirements,

# Maintainer details 
maintainer='Md Slauddin',
maintainer_email='mdslauddin285@gmail.com',

#packages
zip_safe=False,
classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),

python_requires='>=3.5',
)




def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('riyazi', parent_package, top_path)
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup

    config = configuration(top_path='').todict()
    setup(**config)


