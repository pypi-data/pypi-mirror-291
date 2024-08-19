from setuptools import setup, find_packages

setup(
    name='iAppFlyer',
    version='1.0.9',
    author='Karthick Kumar Gopalakrishnan',
    author_email='karthickkumar1996@gmail.com',
    description='A Tkinter application for distributing iOS builds via AppCenter.',
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Finds all packages in `iAppFlyer/`
    include_package_data=True,
    install_requires=[
        'Pillow',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'iAppFlyer = iAppFlyer.main:main',  # Assumes `main()` is defined in `main.py`
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)