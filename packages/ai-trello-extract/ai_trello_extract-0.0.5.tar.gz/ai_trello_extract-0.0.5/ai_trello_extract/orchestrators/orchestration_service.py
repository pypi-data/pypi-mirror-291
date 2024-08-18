import json
import os
from datetime import datetime
from itertools import groupby

from ai_trello_extract.formatters.generate_markdown import generate_markdown
from ai_trello_extract.services.trello_service import TrelloService


class OrchestrationService:
    def __init__(self, trello_service: TrelloService):
        """
        Initializes the OrchestrationService with a TrelloService instance.

        Args:
            trello_service (TrelloService): The service to interact with Trello API.
        """
        self.trello_service = trello_service

    def write_board_markdown_to_file(self, board_name: str, directory: str) -> str:
        """
        Generates markdown for a Trello board and writes it to a file.

        Args:
            board_name (str): The name of the Trello board.
            directory (str): The directory where the file will be saved.

        Returns:
            str: The path to the file where the markdown was written.
        """
        markdown_content = self.get_board_markdown(board_name)
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(directory, f"{board_name} Status Trello Board.txt")
        with open(file_path, "w") as file:
            file.write(markdown_content)  # Write the markdown content to the file
        return file_path

    def write_board_markdown_to_directory(self, board_name: str, directory: str) -> str:
        """
        Generates markdown for a Trello board, splits it into sections, and writes each section to a separate file.

        Args:
            board_name (str): The name of the Trello board.
            directory (str): The directory where the files will be saved.

        Returns:
            str: The path to the directory where the markdown files were written.
        """
        dir_path = os.path.join(directory, f"{board_name} Status Trello Board")
        os.makedirs(dir_path, exist_ok=True)  # Ensure the directory exists

        markdown_content = self.get_board_markdown(board_name)
        transformed_markdown_content = self._extract_markdown_into_collections(markdown_content)

        for title, content in transformed_markdown_content:
            file_path = os.path.join(dir_path, f"{board_name} Trello Status {title}.txt")
            with open(file_path, "w") as file:
                file.write(content)  # Write each section's content to a separate file

        return dir_path

    def _extract_markdown_into_collections(self, markdown_content: str) -> list[tuple[str, str]]:
        """
        Extracts lines starting with H1 headers and their content into a list of tuples.

        Args:
            markdown_content (str): The markdown content to process.

        Returns:
            list[tuple[str, str]]: A list of tuples where each tuple contains the header and its content.
        """
        lines = markdown_content.split("\n")
        headers_and_content = self._extract_title_and_content(lines)

        return headers_and_content

    def _extract_title_and_content(self, lines):
        """
        Groups lines by headers and their content.

        Args:
            lines (list[str]): The lines of markdown content.

        Returns:
            list[tuple[str, str]]: A list of tuples where each tuple contains the header and its content.
        """
        grouped_lines = groupby(lines, key=lambda line: line.startswith("# "))
        headers = [
            (header[2:], f"{datetime.now().strftime('%m-%d-%Y')}\n\n{header}\n" + "\n".join(content).strip())
            for is_header, group in grouped_lines
            if is_header
            for header in group
            for _, content in [next(grouped_lines, (False, []))]
        ]

        return headers

    def get_board_markdown(self, board_name: str) -> str:
        """
        Retrieves the markdown representation of a Trello board.

        Args:
            board_name (str): The name of the Trello board.

        Returns:
            str: The markdown content of the board.
        """
        board = self.trello_service.get_board_by_name(board_name)
        return generate_markdown(self.trello_service.extract_cards_info(board))

    def write_board_json_to_file(self, board_name: str, directory: str) -> str:
        """
        Retrieves the JSON representation of a Trello board and writes it to a file.

        Args:
            board_name (str): The name of the Trello board.
            directory (str): The directory where the file will be saved.

        Returns:
            str: The path to the file where the JSON was written.
        """
        board_json = self.get_board_json(board_name)

        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(directory, f"{board_name} Trello.json")
        with open(file_path, "w") as file:
            json.dump(board_json, file, indent=2)  # Write the JSON content to the file

        return file_path

    def get_board_json(self, board_name: str) -> dict:
        """
        Retrieves the JSON representation of a Trello board.

        Args:
            board_name (str): The name of the Trello board.

        Returns:
            dict: The JSON content of the board.
        """
        board = self.trello_service.get_board_by_name(board_name)
        categorized_lists = self.trello_service.extract_cards_info(board)
        return categorized_lists.to_dict()
