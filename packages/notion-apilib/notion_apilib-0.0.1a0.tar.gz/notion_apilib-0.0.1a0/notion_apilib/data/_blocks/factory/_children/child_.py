# Standard Library
from typing import Optional, Type, TypeVar

# First Party
from notion_apilib.data.structures import Parent

from ...block import Block
from ...data import ChildDatabase, ChildPage, block_structures
from .._general import _create_block

T = TypeVar("T", ChildDatabase, ChildPage)


def create_child_block(
        child_type: Type[T],
        parent: Parent,
        title: str,
        children: Optional[list[Block]] = None,
) -> T:
    """
    Factory method to create a child block object.

    :param child_type: The type of the child block (ChildDatabase or ChildPage).
    :param parent: The parent object.
    :param title: The title of the child block.
    :param children: List of child blocks (optional).
    :return: A new child block object of the specified type.
    """
    return _create_block(
        child_type,
        parent=parent,
        children=children,
        block_type_specific_params=block_structures.ChildAttributes(title=title),
    )


def create_child_database(
        parent: Parent, title: str, children: Optional[list[Block]] = None
) -> ChildDatabase:
    """
    Factory method to create a ChildDatabase object.

    :param parent: The parent object.
    :param title: The title of the child database.
    :param children: List of child blocks (optional).
    :return: A new ChildDatabase object.
    """
    return create_child_block(ChildDatabase, parent, title, children)


def create_child_page(
        parent: Parent, title: str, children: Optional[list[Block]] = None
) -> ChildPage:
    """
    Factory method to create a ChildPage object.

    :param parent: The parent object.
    :param title: The title of the child page.
    :param children: List of child blocks (optional).
    :return: A new ChildPage object.
    """
    return create_child_block(ChildPage, parent, title, children)


__all__ = ["create_child_page", "create_child_database"]
