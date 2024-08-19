from setuptools import setup

setup(
    name='iAppFlyer',
    version='1.0.8',
    author='Karthick Kumar Gopalakrishnan',
    author_email='karthickkumar1996@gmail.com',
    description='A Tkinter application for distributing iOS builds via AppCenter.',
    long_description_content_type='text/markdown',
    py_modules=['iAppFlyer'],  # Specify the script directly
    install_requires=[
        'Pillow',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'iAppFlyer = iAppFlyer:main',  # Adjust to match your script's structure
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)