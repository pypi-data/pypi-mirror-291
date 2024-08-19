from setuptools import setup, find_packages

setup(
    name="py_thumbpad",
    version="1.0.3",
    author="kerodekroma",
    author_email="kerodekroma@gmail.com",
    description="A virtual thumb pad for directional input, featuring a central donut shape and a movable button pad.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/kerodekroma/py-thumbpad",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pygame>=2.0.0',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'py_thumbpad=py_thumbpad.main:main',
        ],
    },
)