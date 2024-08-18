"""
The `_structures` package is an internal package used to hide the implementation details of the factory methods
and data models used for various Notion API JSON payload objects. It provides the logic for instantiating and
validating these objects, ensuring they are created and validated with the necessary attributes and rules.

Purpose:
    - Define internal factory methods for creating instances of various data structures used in the Notion API.
    - Define internal data models for these data structures to ensure data integrity and consistency.
    - Hide the implementation details from the public API to provide a cleaner and more user-friendly interface.

Implementation Details:
    - The package includes internal factory methods and data models for various data structures, including files,
      icons, mentions, parents, text, and user-related structures.
    - Each factory method is designed to instantiate and return an object with default values and any necessary
      validations, leveraging Pydantic models for data integrity.
    - Each data model is implemented as a Pydantic model, providing automatic validation and serialization, and
      defining the attributes and types for each object to ensure all required fields are present and correctly typed.

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

Data Classes:
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

Note:
    This package is intended for internal use only to simplify the creation and validation of Notion API data
    structures. It hides the implementation details from the public API, providing a cleaner and more user-friendly
    interface for developers.
"""
