from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='PatchCreator',
    url='https://github.com/hudikm/patchcreator',
    author='Martin Hudik',
    author_email='martin.hudik@fri.uniza.sk',
    # Needed to actually package something
    packages=['patchcreator'],
    # Needed for dependencies
    install_requires=['asciitree'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Simple script for generating json pach file used in Generator script',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    scripts=['patchcreator/patchcreator.py']
)
