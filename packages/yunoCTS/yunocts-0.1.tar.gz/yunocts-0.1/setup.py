from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='yunoCTS',
    version='0.1',
    license='MIT License',
    author='SDK_PS',
    url='https://pypi.org/project/yunocts',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='payments@monetizze.com.br',
    keywords='yuno',
    description=u'SDK Yuno',
    packages=['yunoCTS'],)
