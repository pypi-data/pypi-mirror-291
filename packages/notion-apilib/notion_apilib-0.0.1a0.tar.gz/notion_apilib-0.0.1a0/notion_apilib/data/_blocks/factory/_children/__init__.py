"""
The `_factory.children` package contains factory methods for creating block objects that can have children in the Notion API.
This package is used to differentiate between _blocks that can have children and those that cannot.

Purpose:
    - Provide factory methods to create instances of block objects that can have children for the Notion API.
    - Simplify the creation process of child-supporting _blocks by encapsulating the creation logic.

Implementation Details:
    - The package includes factory methods for various block types that can have children, such as child pages,
      child databases, headings, list items, and other child-supporting _blocks.

Factory Methods:
    - create_child_page
    - create_child_database
    - create_heading1
    - create_heading2
    - create_heading3
    - create_bulleted_list_item
    - create_numbered_list_item
    - create_to_do
    - create_quote
    - create_toggle
    - create_paragraph
    - create_synced_block
    - create_callout
    - create_table
    - create_table_row
    - create_column
    - create_table_of_contents

Note:
    This package is intended for internal use within the library to support the creation
    of block objects that can have children. It is not intended to be used directly by end-users.
"""
