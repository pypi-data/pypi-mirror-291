# AI Trello Extract

Trello Extract is a Python project that uses the py-trello library and python-dotenv to authenticate with the Trello API and fetch details from Trello boards, lists, and cards. This project demonstrates how to securely manage API credentials and interact with Trello's API to retrieve project data for further processing.

## Features

- Authenticate with the Trello API using OAuth.
- Fetch details of all accessible Trello boards.
- Retrieve lists and cards from a specified Trello board.
- Securely manage API credentials using environment variables.

## Install through PyPI

```bash
pip install ai-trello-extract
```

For more details, visit the [PyPI project page](https://pypi.org/project/ai-trello-extract/).

## Setup

### 1: Register for Trello API Access

1. **Sign Up for a Trello Account**:

   - If you don't have a Trello account, sign up at [Trello](https://trello.com/).

2. **Get API Key and Token**:
   - Go to the [Trello Developer Portal](https://trello.com/app-key).
   - Copy your API Key.
   - Click on the "Token" link to generate a token. This token will be used for authentication in your API requests.

### 2. Clone the repository:

```bash
git clone https://github.com/DEV3L/ai-trello-extract
cd ai-trello-extract
```

Copy the env.local file to a new file named .env and replace the placeholder environment variables with your actual Trello API key:

```bash
cp env.default .env
```

#### Environment Variables

The following environment variables can be configured in the `.env` file:

- `TRELLO_API_KEY`: The Trello API key
- `TRELLO_API_TOKEN`: The Trello API token
- `TRELLO_BOARD_NAME`: The Trello board name
- `OUTPUT_DIRECTORY`: The output directory

### 3. Setup a virtual environment with dependencies and activate it:

```bash
brew install hatch
hatch env create
hatch shell
```

#### Usage

The `run_end_to_end.py` script will:

1. Authenticate with the Trello API using the credentials provided in the `.env` file.
2. Fetch and print the details of all accessible Trello boards.
3. Fetch and print the lists and cards from the first Trello board in the list.

## Testing

### End to End Test

```bash
hatch run e2e
```

### Unit Tests

```bash
hatch run test
```

### Coverage Gutters:

```bash
Command + Shift + P => Coverage Gutters: Watch
```

## Example

Example Trello Board: [AI Trello Extract Example](https://trello.com/invite/b/66bb5639bc7ede83da207f39/ATTId6fc81bc36d22d92f14c3943b237d19cE7C5BFE1/ai-trello-extract-example)

## Example Program

```
from loguru import logger

from ai_trello_extract.clients.trello_client import get_trello_client
from ai_trello_extract.env_variables import ENV_VARIABLES, set_env_variables
from ai_trello_extract.orchestrators.orchestration_service import OrchestrationService
from ai_trello_extract.services.trello_service import TrelloService


def main():
    orchestration_service = OrchestrationService(
        TrelloService(get_trello_client(ENV_VARIABLES.trello_api_key, ENV_VARIABLES.trello_api_token))
    )

    try:
        markdown_file_name = orchestration_service.write_board_markdown_to_file(
            ENV_VARIABLES.trello_board_name, ENV_VARIABLES.output_directory
        )
        logger.info(f"Markdown file written to file {markdown_file_name}")

        markdown_directory_name = orchestration_service.write_board_markdown_to_directory(
            ENV_VARIABLES.trello_board_name, ENV_VARIABLES.output_directory
        )
        logger.info(f"Markdown file written to directory {markdown_directory_name}")
    except RuntimeError as e:
        logger.error(e)


if __name__ == "__main__":
    set_env_variables()
    main()
```

### Example Directory Output

```
AI Trello Extract Example Status Trello Board/
├── AI Trello Extract Example Trello Status BACKLOG.txt
        | 08-17-2024
        |
        | # BACKLOG
        | This is a list of cards, work items, user stories, and tasks that are in the backlog |--category.
        |
        | ## Title: Integrate into other projects
        |
        | ## List Name: Backlog
        |
        | ## Labels
        |
        | - Future
├── AI Trello Extract Example Trello Status DOING.txt
├── AI Trello Extract Example Trello Status DONE.txt
└── AI Trello Extract Example Trello Status TODO.txt
```

### Example File Output

```
# BACKLOG

This is a list of cards, work items, user stories, and tasks that are in the backlog category.

## Title: Integrate into other projects

## List Name: Backlog

## Labels

- Future

# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

## Title: Test and Make Sure It Works

## List Name: Todo

## Labels

- Testing

## Description

Need to verify the code works as planned

# DOING

This is a list of cards, work items, user stories, and tasks that are in the doing category.

## Title: Upload to PyPI

## List Name: Doing

## Labels

- Code

# DONE

This is a list of cards, work items, user stories, and tasks that are in the done category.

## Title: Make new project

## List Name: Done

## Labels

- Code

## Description

Create the project for uploading to PyPI

### Comments

Use existing ai-assistant-manager project as a base
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Ensure all tests pass.
5. Submit a pull request with a detailed description of your changes.

## Code of Conduct

We expect all contributors to adhere to our Code of Conduct:

- Be respectful and considerate.
- Avoid discriminatory or offensive language.
- Report any unacceptable behavior to the project maintainers.

By participating in this project, you agree to abide by these guidelines.
