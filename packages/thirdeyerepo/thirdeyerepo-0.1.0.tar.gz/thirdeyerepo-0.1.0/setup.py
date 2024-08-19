from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="thirdeyerepo",  # Replace with your package's name
    version="0.1.0",  # Initial release version
    author="Jack Ma",  # Your name or organization
    author_email="jackma98004@gmail.com",  # Your contact email
    description="Test",  # Short description of your package
    long_description=long_description,  # Load README.md as long description
    long_description_content_type="text/markdown",  # Set the content type for long_description
    url="https://github.com/allestech/thirdeyerepo",  # URL to the project's homepage or repository
    packages=find_packages(),  # Automatically find all packages and subpackages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose a license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
    install_requires=[
        "requests>=2.20",  # External dependencies, add more as needed
    ],
    # entry_points={
    #     'console_scripts': [
    #         'my_command=my_package.module:main_function',  # Example command-line tool
    #     ],
    # },
)
