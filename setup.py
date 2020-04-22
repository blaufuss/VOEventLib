from setuptools import setup, find_packages

setup(
    name='VOEventLib',
    version='1.3_dev',
    url='https://git.ligo.org/emfollow/VOEventLib',
    description='Python library to read, modify, and create VOEvents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    packages=find_packages(),
    python_requires='>=3.5',
)
