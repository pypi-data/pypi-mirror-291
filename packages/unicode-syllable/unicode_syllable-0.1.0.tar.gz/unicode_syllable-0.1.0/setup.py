from setuptools import setup, find_packages

setup(
    name='unicode_syllable',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    author='Khant Kyaw',
    author_email='khantkyaw6339@gmail.com',
    description='Unicode Syllable break',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/khantkyaw6339/Unicode_Syllable_Break',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license="MIT",
)