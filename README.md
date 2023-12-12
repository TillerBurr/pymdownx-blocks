# PyMdown Extensions Blocks

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![PyPI - Version](https://img.shields.io/pypi/v/pymdownx-blocks)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymdownx-blocks)
![Tests](https://img.shields.io/github/actions/workflow/status/TillerBurr/pymdownx-blocks/tests)



These are a collection of blocks for the [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions) that I find useful.

This project is not affiliated with the PyMdown Extensions project and is currently in a very early stage. Currently, there is only one block: `DirTree`.

## Installation

```bash
pip install pymdownx-blocks
```

## Usage
This can be used in MkDocs or by itself. To use in a Python file, we use the following:

```python
import markdown

yaml_str=...
md=markdown.Markdown(extensions=['pymdownx_blocks.dirtree'])
```

To use in MkDocs, register the extension.

```yaml
...
markdown_extensions:
...
- pymdownx_blocks.dirtree
...
```

In a markdown file, 
```
///dirtree

root:
- subdir:
  - File
- another subdir:
  - anotherfile.txt
  - file.csv
///
```


When rendered, this will produce the following tree

<div>
<pre class="admonition note"><p class="admonition-title">Directory Structure</p>
<p> 
root
├── subdir 
│   └── File
└── another subdir
    ├── anotherfile.txt 
    └── file.csv
</p></pre>
</div>


## Contributing 

More blocks are always welcome! This project uses [rye](https:rye-up.com) for dependency
management.

1. Fork the repository
2. Create a branch with the name of the block
3. Implement the block
4. Create a pull request.
