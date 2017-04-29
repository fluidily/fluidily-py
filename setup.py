from setuptools import setup, find_packages

import fluidily


meta = dict(
    name='fluidily-py',
    version=fluidily.__version__,
    author='Luca Sbardella',
    author_email="luca@quantmind.com",
    maintainer_email="luca@quantmind.com",
    url="https://github.com/fluidily/fluidily-py",
    license="BSD",
    packages=find_packages(include=['fluidily', 'fluidily.*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)


if __name__ == '__main__':
    setup(**meta)
