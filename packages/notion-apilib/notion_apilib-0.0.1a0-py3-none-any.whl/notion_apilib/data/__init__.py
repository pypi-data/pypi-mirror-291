"""
This package provides a streamlined interface for interacting with the Notion API. It includes a set of Python classes, factory methods, and validation mechanisms that abstract the complex Notion API into a more intuitive and Pythonic Domain-Specific Language (DSL). This allows developers to easily create, manipulate, and validate Notion objects without needing to delve into the underlying API details.

### Package Structure:

- **blocks**:
    Contains classes and factory methods representing various types of Notion blocks, such as paragraphs, headings, and lists. These blocks are the fundamental building units in Notion and are validated using Pydantic to ensure they conform to Notion's API structure.

- **structures**:
    Houses low-level structural objects that are commonly used within Notion blocks and properties. These include entities like `RichText`, `Annotations`, and others that are essential for constructing valid Notion API objects.

- **properties**:
    Includes classes and factory methods for Notion page and database properties, as well as `Page` and `Database` objects. This module provides an easy interface for creating and manipulating pages and databases within Notion.

### Core Components:

- **Page** and **Database**:
    High-level classes representing Notion pages and databases, with associated properties and methods for easy manipulation.

- **Factory Methods**:
    - `deserialize_page`: Converts JSON into a `Page` object.
    - `deserialize_database`: Converts JSON into a `Database` object.

### Key Features:

- **Schema Enforcement**: All classes use Pydantic to enforce schema rules, ensuring that the data conforms to Notion's API structure.
- **Factory Methods**: Simplify object creation and reduce manual configuration, making it easier for developers to work with Notion objects.
- **Custom DSL**: Provides a Pythonic interface to the Notion API, enhancing code readability and maintainability.

This package is ideal for developers looking to interact with the Notion API in a more intuitive, error-resistant manner, offering a high level of abstraction and ease of use.
"""

from .configuration_ import BasicConfiguration, ExtraConfiguration
from .database_ import Database, deserialize_database
from .object_ import MajorObject, Object
from .page_ import Page, deserialize_page
from .properties_structure import PropertiesStructure

__all__ = [
    "Page",
    "Database",
    "ExtraConfiguration",
    "BasicConfiguration",
    "deserialize_page",
    "deserialize_database",
    "PropertiesStructure",
    "Object",
    "MajorObject",
]
