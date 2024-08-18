from setuptools import setup, find_packages

setup(
    name='revitic_ddos',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'concurrent.futures',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'revitic_ddos=revitic_ddos.core:run_ddos',
        ],
    },
    author='Eren Ceylan',
    author_email='notrevitic@gmail.com',
    description='A simple DDOS tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/revitic_ddos',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
