from functools import reduce

from loguru import logger
from trello import Board, TrelloClient
from trello import List as TrelloList

from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard
from ai_trello_extract.functions import first
from ai_trello_extract.services.trello_utilities import extract_card_info, trello_list_reducer


def extract_card_info_from_list(trello_list: list[TrelloList]) -> list[TrelloCard]:
    """
    Extracts card information from a list of Trello lists.

    Args:
        trello_list (list[TrelloList]): A list of Trello lists.

    Returns:
        list[TrelloCard]: A list of TrelloCard dataclasses containing the extracted card information.
    """
    return [extract_card_info(trello_list, card) for trello_list in trello_list for card in trello_list.list_cards()]


class TrelloService:
    def __init__(self, client: TrelloClient):
        """
        Initializes the TrelloService with a Trello client.

        Args:
            client (TrelloClient): The Trello client to interact with the Trello API.
        """
        self.client = client

    def extract_cards_info(self, board: Board) -> CategorizedLists[TrelloCard]:
        """
        Extracts card information from a Trello board and categorizes it.

        Args:
            board (Board): The Trello board to extract card information from.

        Returns:
            CategorizedLists[TrelloCard]: A dataclass containing categorized lists of Trello cards.
        """
        categorized_lists = self.categorize_lists(board)

        logger.debug(f"Extracting Trello Cards from categorized lists: {categorized_lists}")

        planning = extract_card_info_from_list(categorized_lists.backlog)
        todo = extract_card_info_from_list(categorized_lists.todo)
        doing = extract_card_info_from_list(categorized_lists.doing)
        done = extract_card_info_from_list(categorized_lists.done)

        return CategorizedLists(backlog=planning, todo=todo, doing=doing, done=done)

    def categorize_lists(self, board: Board) -> CategorizedLists[TrelloList]:
        """
        Categorizes the lists of a Trello board.

        Args:
            board (Board): The Trello board to categorize lists from.

        Returns:
            CategorizedLists[TrelloList]: A dataclass containing categorized Trello lists.
        """
        trello_lists = self.get_lists_for_board(board)
        filtered_trello_lists = filter(lambda trello_list: "_" != trello_list.name, trello_lists)
        return reduce(
            trello_list_reducer,
            filtered_trello_lists,
            CategorizedLists[TrelloList](backlog=[], todo=[], doing=[], done=[]),
        )

    def get_board_by_name(self, board_name: str) -> Board:
        """
        Retrieves a Trello board by its name.

        Args:
            board_name (str): The name of the Trello board to retrieve.

        Returns:
            Board: The Trello board with the specified name.

        Raises:
            RuntimeError: If the board with the specified name is not found.
        """
        boards = self._list_boards()
        board = first(filter(lambda board: board.name == board_name, boards))

        if not board:
            raise RuntimeError(f"Board with name '{board_name}' not found.")

        return board

    def get_lists_for_board(self, board: Board) -> list[TrelloList]:
        """
        Retrieves all lists for a given Trello board.

        Args:
            board (Board): The Trello board to retrieve lists from.

        Returns:
            list[TrelloList]: A list of Trello lists from the specified board.
        """
        logger.debug(f"Listing Trello Lists for board: {board.name}")
        return board.all_lists()

    def _list_boards(self) -> list[Board]:
        """
        Retrieves all boards for the Trello client.

        Returns:
            list[Board]: A list of all Trello boards.
        """
        logger.debug("Listing Trello Boards")
        return self.client.list_boards()
