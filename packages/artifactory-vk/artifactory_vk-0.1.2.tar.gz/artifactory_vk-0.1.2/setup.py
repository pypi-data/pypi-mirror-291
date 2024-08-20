from pathlib import Path
from setuptools import find_packages, setup


setup(
    name='artifactory-vk',
    version='0.1.2',
    python_requires='>=3.10',
    packages=find_packages(),
    install_requires=[
        'pydantic~=2.8.2',
        'requests~=2.32.3',
        'tuspy~=1.0.3',
    ],
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown'
)
