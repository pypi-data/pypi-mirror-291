from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    requirements = []
    try:
        with open(file_path, 'r') as file_obj:
            requirements = file_obj.readlines()  # Read lines from the file
            requirements = [req.strip() for req in requirements]  # Strip whitespace and newlines
            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
    except FileNotFoundError:
        print(f"Warning: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return requirements


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mongopackage110",
    version='0.1.0',
    author='Ali Pourranjbar',
    description='My first python package',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Added to specify markdown format
    author_email='a_pourranjbar@rocketmail.com',
    url='https://github.com/alipourranjbar/Myfirstpackage.git',
    install_requires=get_requirements('requirements.txt'),
    package_dir={"": "src"},
    packages=find_packages(where='src'),
)
