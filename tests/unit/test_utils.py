"""Unit tests for parse_markdown_with_frontmatter function."""

from toolfront.utils import parse_markdown_with_frontmatter


def test_parse_markdown_with_commands():
    """Test parsing markdown with command frontmatter."""
    markdown = """---
- [python3, script.py]
- [bash, ls, -la]
---
# Title

Some content"""

    body, commands = parse_markdown_with_frontmatter(markdown)
    assert body == "# Title\n\nSome content"
    assert commands == [["python3", "script.py"], ["bash", "ls", "-la"]]


def test_parse_markdown_without_frontmatter():
    """Test parsing markdown without frontmatter."""
    markdown = "# Title\n\nSome content"
    body, commands = parse_markdown_with_frontmatter(markdown)
    assert body == markdown
    assert commands == []


def test_parse_markdown_with_invalid_yaml():
    """Test that invalid YAML frontmatter returns original content."""
    markdown = """---
[this is: invalid yaml
---
# Title"""

    body, commands = parse_markdown_with_frontmatter(markdown)
    # When YAML parsing fails, it returns the original markdown
    assert body == markdown
    assert commands == []  # Falls back to empty list on parse error
