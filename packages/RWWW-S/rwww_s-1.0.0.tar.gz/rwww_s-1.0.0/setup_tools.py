from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.12'
]

setup(
    name='RWWW_S',
    version='1.0.0',
    description='A removal tool for removing www and https://www. from dictionary\'s',
    long_description_content_type='text/markdown',
    long_description=open('CHANGE.LOG.md').read() + '\n\n' + open('README.md').read(),
    url='https://github.com/IEYT/RW-s',  
    author='Manveer Singh',
    author_email='manveer1113@outlook.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='RemoveWWW', 
    packages=find_packages(),
    install_requires=[""] 
)