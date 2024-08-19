from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gptlite',
    version='0.0.2',
    author='LLMApp Group',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': ['setuptools', 'wheel', 'twine']
    },
    # entry_points={
    #     'console_scripts': [
    #         'gptlite=apps.cli:cli',
    #     ],
    # },
)
