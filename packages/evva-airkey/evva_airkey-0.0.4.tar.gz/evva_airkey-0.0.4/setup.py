import setuptools

short_desc = (
    'Communication module for EVVA Airkey cloud integration'
)
long_desc = open("README.md").read()

setuptools.setup(
    name='evva_airkey',
    version='0.0.4',
    packages=('evva_airkey', ),

    description=short_desc,
    long_description=long_desc,
    long_description_content_type='text/markdown',

    # url git
    url='https://gitlab.com/geusebi/evva_airkey',

    python_requires='>=3.6',
    install_requires=('requests', ),

    author='Giampaolo Eusebi',
    author_email='giampaolo.eusebi@gmail.com',

    license='GNU LGPL 3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
)
