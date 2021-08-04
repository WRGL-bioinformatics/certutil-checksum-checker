![WRGL logo](/source/images/wrgl_logo.png "WRGL logo")

# checksum_checker

Python script to check backup hashes which have been createds with certUtil but don't have a simple checking function available.

## TODO

Update the README To include more usage, maybe some images, and also installation instructions (e.g. using pyinstaller)

## Usage

_TODO: Add some screenshots_

## Installation

This tool is intended to be packaged as a single executable file using PyInstaller.

`python -m PyInstaller --clean checksum_checker.spec`

To reduce unecessary overheads when pushing updates, PyInstaller is not included in requirements.txt It should be installed when needed.

Before packaging, ensure the code has been pushed and passes all CI tests. Ideally, run _black_ to format all code consistently with PEP-8.

## Tests

A small number of tests have been included as an aid for future development. Code coverage is not 100%, nor is it ever likely to be 100% - as that is not my goal and it isn't needed.

GitLab has been configured, through the .gitlab-ci.yml file, to run the following tests after a push:

* Static code analysis:
  * flake8 - Style guide enforcement (PEP-8)
  * mypy - Type checking (requires var types to be explicitly defined in the code)
  * pylint - Code error analysis, standard enforcement, & code smells.
* Unit testing:
  * pytest - runs defined unit test from app/tests/rest_read_checksum_file.py
  * pytest-cov - Adds test coverage percentage