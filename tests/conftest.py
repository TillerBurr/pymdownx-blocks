import pytest
import markdown
from typing import Any


@pytest.fixture
def markdown_fixture():
    def _method(
        extensions: list[str] | str, extension_config: dict[str , dict[str, Any]]
    ):
        """Fixture to dynamically insert markdown extensions."""
        return markdown.Markdown(
            extensions=extensions, extension_configs=extension_config
        )

    return _method
