from setuptools import setup, find_packages

setup(
    name='spotifyfizyfit',
    version='1.0.8',
    description='spotifyfizyfit, a tool to migrate your Spotify playlists',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fleizean/spotifyfizyfit',
    author='fleizean (Enes Yagiz)',
    author_email='nsyagz@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'colorama',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
    ],
    keywords=['spotify fizy playlist migration'],
    entry_points={
        'console_scripts': [
            'spotifyfizyfit=spotifyfizyfit.runner:run',
        ],
    },
)