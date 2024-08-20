from setuptools import setup, find_packages


setup(

    name='tse_derivatives',

    version='0.1.4',

    packages=find_packages(),

    install_requires=['requests','pandas'],  # List dependencies here

    author='Jalal Seifoddini',

    author_email='jalal.seifoddini@gmail.com',

    description='Gets the underlying asset ticker and the option type (either call or put) to fetch live option data.',

    long_description=open('README.md', encoding="utf-8").read(),

    long_description_content_type='text/markdown',

    classifiers=[

        'Programming Language :: Python :: 3',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

    ],

    python_requires='>=3.6',

)