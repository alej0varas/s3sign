from setuptools import setup

setup(
    name="s3sign",
    version=__import__('s3sign').__version__,
    author="Alexandre Varas",
    author_email="alej0varas@gmail.com",
    py_modules=['s3sign', ],
    include_package_data=True,
    license='GNU Library or Lesser General Public License (LGPL)',
    description="A library to generate AWS S3 Signed Requests",
    url='https://github.com/alej0varas/s3sign',
    install_requires=[],
    tests_require = ['requests', ],
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
