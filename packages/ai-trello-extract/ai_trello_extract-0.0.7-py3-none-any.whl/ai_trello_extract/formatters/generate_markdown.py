from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard
from ai_trello_extract.formatters.escape_markdown import escape_markdown


def generate_markdown(categorized_lists: CategorizedLists[TrelloCard]) -> str:
    """
    Generates markdown text from categorized Trello cards.

    Args:
        categorized_lists (CategorizedLists[TrelloCard]): The categorized lists of Trello cards.

    Returns:
        str: The generated markdown text.
    """
    # Extract non-empty categories and their cards from the categorized lists
    list_items = [
        (category, cards)
        for category, cards in categorized_lists.__dict__.items()
        if category in categorized_lists.__dataclass_fields__ and cards
    ]

    # Format each category and its cards into markdown lines
    markdown_lines = [line for category, cards in list_items for line in format_category(category, cards)]
    return "\n".join(markdown_lines)


def format_category(category: str, cards: list[TrelloCard]) -> list[str]:
    """
    Formats a category and its cards into markdown lines.

    Args:
        category (str): The category name.
        cards (list[TrelloCard]): The list of Trello cards in the category.

    Returns:
        list[str]: The formatted markdown lines for the category and its cards.
    """
    # Create a header for the category and format each card
    return [
        f"# {category.upper()}\n\nThis is a list of cards, work items, user stories, and tasks that are in the {category} category.",
        "",
    ] + [line for card in cards for line in format_card(card)]


def format_card(card: TrelloCard) -> list[str]:
    """
    Formats a Trello card into markdown lines.

    Args:
        card (TrelloCard): The Trello card to format.

    Returns:
        list[str]: The formatted markdown lines for the card.
    """
    # Format each attribute of the card into markdown lines if it exists
    title_lines = [f"## Title: {card.title}", ""] if card.title else []
    list_name_lines = [f"### List Name: {card.list_name}", ""] if card.list_name else []
    labels_lines = ["### Labels", ""] + [f"- {label}" for label in card.labels] + [""] if card.labels else []
    done_date_lines = [f"### Done Date: {card.done_date}", ""] if card.done_date else []
    description_lines = ["### Description", "", escape_markdown(card.description), ""] if card.description else []
    comments_lines = (
        ["#### Comments", ""] + [f"{escape_markdown(comment)}\n" for comment in card.comments] if card.comments else []
    )

    # Combine all the formatted lines into a single list
    return title_lines + list_name_lines + labels_lines + done_date_lines + description_lines + comments_lines
