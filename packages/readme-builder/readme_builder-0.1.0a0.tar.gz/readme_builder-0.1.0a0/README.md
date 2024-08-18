## README Generator

This project provides a simple command-line interface (CLI) for generating basic README.md files for software projects. 

### Project Overview

The README Generator aims to simplify the process of creating well-structured README files by automating the generation of essential sections, such as project title, overview, features, installation, usage, license, and contact information. 

### Features

- **Automated README Generation:** Generates a README.md file with basic sections.
- **Project Title Extraction:** Extracts the project title from the directory name.
- **Dependency Detection:** Detects and includes installation instructions based on the presence of `pyproject.toml`.
- **Usage Instructions:** Provides clear usage instructions with example commands.

### Installation

This project uses Poetry for dependency management. To install the project, run the following commands:

```bash
poetry install
```

### Usage

To generate a README.md file, run the following command from the project directory:

```bash
python cli.py
```

This will create a README.md file in the same directory with the generated content.

### License

This project is licensed under the Unlicense. This means that you are free to use, modify, and distribute the software for any purpose, without restrictions.

### Contact Information

For any questions or suggestions, please contact: akshita.dixit1@1mg.com. 
