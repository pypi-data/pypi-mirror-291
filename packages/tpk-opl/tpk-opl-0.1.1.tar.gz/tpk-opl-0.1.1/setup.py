from setuptools import setup, find_packages

setup(
    name="tpk-opl",
    version="0.1.1",
    description="A simple example package",
    author="HouJie",
    author_email="bqdove@gmail.com",
    packages=find_packages(),
    install_requires=[

    ],
    python_requires='>=3.10',

    entry_points={
        'console_scripts': [
            "tpk-opl = tpk.tpk_module:run",
        ]
    }
)
