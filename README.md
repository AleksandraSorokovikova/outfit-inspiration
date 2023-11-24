## Outfit inspiration
Web service for outfit inspiration by your wardrobe

## Configuring dev environment
1. Poetry for dependency management
   1. Create Python 3.11 environment:
           ```
           pyenv install 3.11
           ```
   3. Set which Python to use:
           ```
           poetry env use 3.11
           ```
   4. Install dependencies:
           ```
           poetry install
           ```
2. To check the style run `poetry run black .` in the project root from terminal
3. To check for correct typing run `poetry run mypy .` in the project root from terminal

