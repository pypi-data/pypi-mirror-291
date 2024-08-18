"""
This package provides comprehensive tools for creating and validating Notion API JSON
payload objects. It includes both factory methods for generating complex JSON structures and Pydantic models for
validating these structures. These objects are used throughout the Notion API and include various data structures
that are not blocks or properties.

Purpose:
    - Provide factory methods to create instances of different data structures used in the Notion API.
    - Simplify the instantiation process for developers by offering pre-defined methods to create complex objects
      with minimal effort.
    - Ensure that the created objects adhere to the required structure and validation rules defined by the Notion API.
    - Define data models for various data structures used in the Notion API to ensure data integrity and consistency.
    - Provide a clear and structured representation of the data objects used in the Notion API.

Implementation Details:
    - The package includes factory methods and data models for various data structures, including files, icons, mentions,
      parents, text, and user-related structures.
    - Each factory method is designed to instantiate and return an object with default values and any necessary
      validations, leveraging Pydantic models defined in the corresponding modules to ensure data integrity and
      consistency.
    - The data models are implemented as Pydantic models, providing automatic validation and serialization,
      ensuring that all required fields are present and correctly typed.

Factory Methods:
    - create_file_object
    - create_external
    - create_resources_attributes
    - create_file_attributes
    - create_icon
    - create_emoji
    - create_mention
    - create_template_mention_date
    - create_template_mention_user
    - create_template_mention
    - create_database_mention
    - create_date_mention
    - create_link_preview_mention
    - create_page_mention
    - create_user_mention
    - create_parent
    - create_parent_from_object
    - create_text
    - create_annotations
    - create_rich_text
    - create_link
    - create_basic_rich_text
    - create_basic_annotations
    - create_user
    - create_bot
    - create_people_structure
    - create_people
    - create_owner_structure
    - create_bot_structure
    - create_equation

Data Models:
    - FileObject
    - External
    - FileAttributes
    - ResourcesAttributes
    - Emoji
    - Icon
    - Mention
    - DatabaseMention
    - DateMention
    - LinkPreviewMention
    - UserMention
    - TemplateMention
    - TemplateMentionDate
    - TemplateMentionUser
    - PageMention
    - Parent
    - RichText
    - Text
    - Link
    - Annotations
    - User
    - OwnerStructure
    - PeopleStructure
    - People
    - BotStructure
    - Bot
    - EquationStructure

Types:
    - file_type
    - parents_types

Note:
    This package is intended for use by developers to simplify the creation and validation of Notion API data structures.
    It ensures all objects are created consistently and correctly, adhering to the Notion API's requirements, while also
    validating the data integrity and consistency.
"""

# First Party
from notion_apilib.data._structures.data import (
    Annotations,
    Bot,
    BotStructure,
    DatabaseMention,
    DateMention,
    Emoji,
    EquationStructure,
    External,
    FileAttributes,
    FileObject,
    FormatedText,
    Link,
    LinkPreviewMention,
    Mention,
    OwnerStructure,
    PageMention,
    Parent,
    People,
    PeopleStructure,
    ResourcesAttributes,
    RichText,
    TemplateMention,
    TemplateMentionDate,
    TemplateMentionUser,
    Text,
    User,
    UserMention,
)
from notion_apilib.data._structures.factory import (
    create_annotations,
    create_basic_annotations,
    create_basic_rich_text,
    create_bot,
    create_bot_structure,
    create_database_mention,
    create_date_mention,
    create_emoji,
    create_external,
    create_file_attributes,
    create_file_object,
    create_link,
    create_link_preview_mention,
    create_mention,
    create_owner_structure,
    create_page_mention,
    create_parent,
    create_parent_from_object,
    create_people,
    create_people_structure,
    create_resources_attributes,
    create_rich_text,
    create_template_mention,
    create_template_mention_date,
    create_template_mention_user,
    create_text,
    create_user,
    create_user_mention,
)
from notion_apilib.data._structures.types_ import file_type, parents_types

__all__ = [
    # Factory Methods
    "create_file_object",
    "create_external",
    "create_resources_attributes",
    "create_file_attributes",
    "create_emoji",
    "create_mention",
    "create_template_mention_date",
    "create_template_mention_user",
    "create_template_mention",
    "create_database_mention",
    "create_date_mention",
    "create_link_preview_mention",
    "create_page_mention",
    "create_user_mention",
    "create_parent",
    "create_parent_from_object",
    "create_text",
    "create_annotations",
    "create_rich_text",
    "create_link",
    "create_basic_rich_text",
    "create_basic_annotations",
    "create_user",
    "create_bot",
    "create_people_structure",
    "create_people",
    "create_owner_structure",
    "create_bot_structure",
    # Data Models
    "FileObject",
    "External",
    "FileAttributes",
    "ResourcesAttributes",
    "Emoji",
    "Mention",
    "DatabaseMention",
    "DateMention",
    "LinkPreviewMention",
    "UserMention",
    "TemplateMention",
    "TemplateMentionDate",
    "TemplateMentionUser",
    "PageMention",
    "Parent",
    "RichText",
    "Text",
    "FormatedText",
    "Link",
    "Annotations",
    "EquationStructure",
    "User",
    "OwnerStructure",
    "PeopleStructure",
    "People",
    "BotStructure",
    "Bot",
    # Types
    "file_type",
    "parents_types",
]
