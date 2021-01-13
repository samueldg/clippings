import re

from setuptools import setup


with open('clippings/__init__.py') as f:
    # Not importing the file in setup.py!
    VERSION = re.search(r"__version__ = '(?P<version>.*?)'", f.read()).group('version')


REQUIREMENTS = [
    'python-dateutil~=2.7',
]

setup(
    name='clippings',
    version=VERSION,
    description='Amazon Kindle clippings parser',
    long_description=(open('README.rst').read()),
    long_description_content_type='text/x-rst',
    url='https://github.com/samueldg/clippings/',
    download_url='https://github.com/samueldg/clippings/tarball/' + VERSION,
    install_requires=REQUIREMENTS,
    license='MIT',
    author='Samuel Dion-Girardeau',
    author_email='samuel.diongirardeau@gmail.com',
    packages=[
        'clippings'
    ],
    entry_points={
        'console_scripts': [
            'clippings = clippings.parser:main',
        ],
    },
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=['amazon', 'kindle', 'clipping', 'e-book'],
    zip_safe=False,
)
