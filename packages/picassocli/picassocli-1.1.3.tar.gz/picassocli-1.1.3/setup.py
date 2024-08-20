from setuptools import setup, find_packages
import subprocess
import requests
import sys


DEFAULT_PACKAGE_NAME = 'picassocli'

class VersionAlreadyExistsError(Exception):
    """
    Exception raised when a version already exists on PyPI.
    """
    def __init__(self, version):
        super().__init__(f"Version {version} already exists on PyPI.")
        self.version = version

def get_version():
    """
    Retrieve the latest version tag from Git.

    Returns:
        str: The latest Git tag, or '0.0.0' if an error occurs.
    """
    try:
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], encoding='utf-8').strip()
        return tag
    except subprocess.CalledProcessError:
        return '0.0.0'

def check_version_exists(package_name, version):
    """
    Check if a specific version of a package exists on PyPI.

    Args:
        package_name (str): The name of the package to check.
        version (str): The version to check.

    Returns:
        bool: True if the version exists, False otherwise.
    """
    url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    response = requests.get(url)
    return response.status_code == 200

def main():
    """
    Main function to run the setup process.
    """
    version = get_version()

    if check_version_exists(DEFAULT_PACKAGE_NAME, version):
        raise VersionAlreadyExistsError(version)

    setup(
        name='picassocli',
        version=version,
        description='A utility for constructing ANSI escape codes for terminal text styling.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        author='devinci-it',
        url='https://www.github.com/devinci-it/picassocli',
        packages=find_packages(),
        package_dir={'': '.'},
        install_requires=[
            'huefy',
        ],
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        python_requires='>=3.6',
    )

if __name__ == "__main__":
    try:
        main()
    except VersionAlreadyExistsError as e:
        print(e)
        sys.exit(1)
