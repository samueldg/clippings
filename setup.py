from setuptools import setup

from clippings import __version__

setup(
    name='clippings',
    version=__version__,
    description='Amazon Kindle clippings parser',
    long_description=(open('README.rst').read()),
    url='http://github.com/samueldg/clippings/',
    download_url = 'https://github.com/samueldg/clippings/tarball/' + __version__,
    install_requires=[
        'python-dateutil==2.6.0'
    ],
    license='MIT',
    author='Samuel Dion-Girardeau',
    author_email='samuel.diongirardeau@gmail.com',
    packages=[
        'clippings'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=['amazon', 'kindle', 'clipping', 'e-book'],
    zip_safe=False,
)
