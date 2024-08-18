"""
The `notion-api` package is a high-level library designed to facilitate seamless interaction with the Notion API. It abstracts away the complexities of the API by providing a Domain-Specific Language (DSL) built on top of Pydantic-validated models. This allows developers to work with Notion objects in a Pythonic way, without needing to remember or handle the underlying JSON structure.

### Purpose:
    - **Abstract the Notion API**: Provides an intuitive interface for developers to interact with the Notion API, abstracting the raw JSON structures into easy-to-use Python objects.
    - **Validation with Pydantic**: Ensures data integrity and consistency by leveraging Pydantic for validation, making sure that all interactions with the API conform to Notion's schema.
    - **Simplified API Interaction**: Through the `NotionApi` object, developers can easily manage blocks, pages, and databases within Notion without directly handling API requests.

### Package Structure:
The `notion-api` package is organized into several key components:

- **client**:
    - This module contains the core classes for communicating with the Notion API. These classes—`NotionBlockProvider`, `NotionPageProvider`, and `NotionDatabaseProvider`—handle the creation, retrieval, updating, and deletion of Notion objects.
    - They are designed to work with Pydantic models, ensuring that all data is validated before being sent to the API.
    - While these classes are exposed for documentation purposes, they are managed by the `NotionApi` container and should not be instantiated directly by users.

- **data**:
    - **blocks**: Contains Pydantic models and factory methods for all types of Notion blocks, such as paragraphs, headings, and lists. These blocks are the fundamental building units in Notion.
    - **properties**: Includes models and factory methods for Notion page and database properties, making it easy to manage the metadata and content of Notion objects.
    - **structures**: Provides low-level structures like `RichText`, `Annotations`, and other components that are used within blocks and properties.

### Usage Guide:

1. **Initialize the API**:
    The main entry point for interacting with the Notion API is the `NotionApi` class. This class acts as a container that uses Dependency Injection (DI) principles to manage and provide access to singleton instances of `NotionBlockProvider`, `NotionPageProvider`, and `NotionDatabaseProvider`.

    ```python
    from notion_apilib import NotionApi

    notion_apilib = NotionApi(api_key="your_notion_api_key")
    ```

2. **Access Providers**:
    With the `NotionApi` instance, you can easily access the providers for blocks, pages, and databases:

    ```python
    block_provider = notion_apilib.block_provider()
    page_provider = notion_apilib.page_provider()
    database_provider = notion_apilib.database_provider()
    ```

    These providers should not be instantiated directly. The `NotionApi` container ensures that all dependencies are correctly injected and managed.

3. **Working with Data Models**:
    For creating, validating, and manipulating Notion API objects, the `data` package contains all the necessary Pydantic models and factory methods. You can work with these to build complex Notion objects:

    ```python
    from notion_apilib.data.blocks import ParagraphBlock
    from notion_apilib.data.properties import TitleProperty

    paragraph = ParagraphBlock(text="Hello, Notion!")
    title = TitleProperty(title="My Page")
    ```

### Summary:
The `notion-api` package provides a powerful and intuitive way to interact with the Notion API, abstracting away the complexities of the raw API and offering a Pythonic interface through Pydantic models. By using the `NotionApi` class, developers can easily manage Notion blocks, pages, and databases, while ensuring that all data is validated and consistent with Notion's requirements.

This package is an all-in-one solution for developers looking to integrate with Notion, providing everything needed to work with Notion objects in a clean, maintainable, and Pythonic way.
"""

# First Party
from notion_apilib.notion import NotionApi

from ._client import NotionBlockProvider, NotionDatabaseProvider, NotionPageProvider, ResponseError

__all__ = [
    "NotionApi",
    "NotionBlockProvider",
    "NotionPageProvider",
    "NotionDatabaseProvider",
    "ResponseError",
]
