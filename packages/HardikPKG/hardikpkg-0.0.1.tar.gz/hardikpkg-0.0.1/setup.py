from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Snakegame by Hardik'
LONG_DESCRIPTION = 'A package that allows running a simple snake game developed by Hardik Kansara.'

# Setting up
setup(
    name="HardikPKG",
    version=VERSION,
    author="Hardik Kansara",
    author_email="h.kansara106@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'game', 'snake', 'turtle'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
