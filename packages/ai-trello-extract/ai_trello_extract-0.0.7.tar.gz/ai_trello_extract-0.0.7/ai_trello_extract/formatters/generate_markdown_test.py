from datetime import datetime
from typing import Literal

from ai_trello_extract.dataclasses.categorized_list import CategorizedLists
from ai_trello_extract.dataclasses.trello_card import TrelloCard
from ai_trello_extract.formatters.generate_markdown import generate_markdown


def test_headers():
    """
    Test that generate_markdown correctly generates headers for each category.
    """
    expected_markdown = """# BACKLOG

This is a list of cards, work items, user stories, and tasks that are in the backlog category.

# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

# DOING

This is a list of cards, work items, user stories, and tasks that are in the doing category.

# DONE

This is a list of cards, work items, user stories, and tasks that are in the done category.
"""

    # Create a categorized list with one card in each category
    categorized_list = CategorizedLists(
        backlog=[build_trello_card()],
        todo=[build_trello_card()],
        doing=[build_trello_card()],
        done=[build_trello_card()],
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown matches the expected output
    assert markdown == expected_markdown


def test_card_title_names():
    """
    Test that generate_markdown correctly includes card titles in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

## Title: Title 1

## Title: Title 2
"""

    # Create a categorized list with cards having specific titles
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(title="Title 1"),
            build_trello_card(title="Title 2"),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes the card titles
    assert markdown == expected_markdown


def test_card_list_names():
    """
    Test that generate_markdown correctly includes card list names in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### List Name: List Name 2
"""

    # Create a categorized list with cards having specific list names
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1"),
            build_trello_card(list_name="List Name 2"),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes the card list names
    assert markdown == expected_markdown


def test_card_labels():
    """
    Test that generate_markdown correctly includes card labels in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### Labels

- bug
- urgent
"""

    # Create a categorized list with cards having specific labels
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1", labels=["bug", "urgent"]),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes the card labels
    assert markdown == expected_markdown


def test_card_done_date():
    """
    Test that generate_markdown correctly includes card done dates in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### Done Date: 2024-05-01 00:00:00
"""

    # Create a categorized list with cards having specific done dates
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(
                list_name="List Name 1",
                done_date=datetime(2024, 5, 1, 0, 0),
            ),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes the card done dates
    assert markdown == expected_markdown


def test_card_descriptions():
    """
    Test that generate_markdown correctly includes card descriptions in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

### Description

Description of task 1

### List Name: List Name 2

### Description

#### Description of task 2
"""

    # Create a categorized list with cards having specific descriptions
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1", description="Description of task 1"),
            build_trello_card(list_name="List Name 2", description="# Description of task 2"),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes the card descriptions
    assert markdown == expected_markdown


def test_card_comments():
    """
    Test that generate_markdown correctly includes card comments in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

### List Name: List Name 1

#### Comments

- - -

Comment 1
"""

    # Create a categorized list with cards having specific comments
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(list_name="List Name 1", comments=["---", "Comment 1"]),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes the card comments
    assert markdown == expected_markdown


def test_generate_markdown():
    """
    Test that generate_markdown correctly includes all card attributes in the markdown.
    """
    expected_markdown = """# TODO

This is a list of cards, work items, user stories, and tasks that are in the todo category.

## Title: Title 1

### List Name: List Name 1

### Labels

- bug
- urgent

### Done Date: 2024-05-01 00:00:00

### Description

Description of task 1

#### Comments

Comment 1
"""

    # Create a categorized list with a card having all attributes
    categorized_list = CategorizedLists(
        todo=[
            build_trello_card(
                title="Title 1",
                list_name="List Name 1",
                labels=["bug", "urgent"],
                done_date=datetime(2024, 5, 1, 0, 0),
                description="Description of task 1",
                comments=["Comment 1"],
            ),
        ]
    )

    markdown = generate_markdown(categorized_list)

    # Verify that the generated markdown includes all card attributes
    assert markdown == expected_markdown


def build_trello_card(
    *,
    title="",
    list_name="",
    description="",
    labels: list[str] = [],
    comments: list[str] = [],
    done_date: datetime | Literal[""] = "",
) -> TrelloCard:
    """
    Helper function to build a TrelloCard with default values.

    Args:
        title (str): The title of the card.
        list_name (str): The name of the list the card belongs to.
        description (str): The description of the card.
        labels (list[str]): The labels associated with the card.
        comments (list[str]): The comments on the card.
        done_date (datetime | Literal[""]): The done date of the card.

    Returns:
        TrelloCard: The constructed TrelloCard object.
    """
    return TrelloCard(
        title=title,
        list_name=list_name,
        description=description,
        labels=labels,
        comments=comments,
        done_date=done_date,
    )
