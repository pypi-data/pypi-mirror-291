from setuptools import setup

setup(
    name='iAppFlyer',
    version='1.1.5',
    packages=['iAppFlyer'],
    entry_points={
        'console_scripts': [
            'iAppFlyer=iAppFlyer.main:main',
        ],
    },
    install_requires=[
        'Pillow',
        'requests',
    ],
    include_package_data=True,
    package_data={
        '': ['*.png'],
    },
    zip_safe=False,
)
