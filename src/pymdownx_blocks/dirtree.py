from __future__ import annotations

import xml.etree.ElementTree as etree
from typing import Sequence, TypeAlias, Union

import markdown
import yaml
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block, type_html_identifier


class InvalidYAMLError(BaseException):
    """YAML Cannot be parsed."""


class InvalidTreeError(BaseException):
    """YAML is valid, but not a valid directory tree."""


PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_SPACE = "│   "
SPACE = "    "

TreeNode: TypeAlias = dict[str, Sequence[Union["TreeNode", str]]]


def sorter(x: Union[TreeNode, str]) -> tuple[bool, str]:
    """

    Args:
        x (Union[TreeNode, str]): An element of a TreeNode

    Returns:
        (tuple[bool, str]): A tuple containing a bool that is `True` if x is a `str`,
        and a str containing either `x` or the first (and only) key of `x`

    """
    _type = isinstance(x, str)
    _value = x if isinstance(x, str) else next(iter(x.keys()))
    return _type, _value


class DirTree:
    """
    Create a directory tree from a YAML string.
    """

    def __init__(self, in_: str) -> None:
        """Initialize the tree object.

        Args:
            in_ (str): YAML string

        Raises:
            InvalidTreeError: Not a valid tree.
        """
        try:
            self.tree = yaml.safe_load(in_)
            if not isinstance(self.tree, dict):
                raise InvalidTreeError("A tree must have a key:value pair")
            if isinstance(self.tree, dict) and len(list(self.tree.keys())) != 1:
                raise InvalidTreeError("A tree can have only one root directory.")
        except yaml.error.YAMLError:
            raise InvalidYAMLError

    def build(
        self,
        tree: TreeNode,
        current_index: int = 0,
        prefix: str = "",
        parent_siblings: int = 0,
        item_sep: str = "",
        is_root: bool = True,
    ) -> str:
        """
        Build the output. The final result is a string containing the tree.

        Args:
            tree (TreeNode): A node in the tree. It is a dict containing values that are
            a list of strings or dictionaries.
            current_index (int): Current index of the item in the sequence.
            prefix (str): String that is prepended to each line.
            parent_siblings (int): Number of siblings the parent has.
            item_sep (str): An Elbow or Tee. Used between lines, next to items.
            is_root (bool): Declares the root of the tree.

        Returns:
            A string containing the parsed tree.
        """
        _tree = ""
        directory = next(iter(tree.keys()))
        contents = tree.get(directory, [])
        # At root
        if is_root:
            _tree += f"{directory}\n"
        else:
            _tree += f"{prefix}{item_sep}{directory}\n"

        # Files are last
        sorted_contents = sorted(contents, key=sorter)
        num_siblings = len(contents) - 1

        # Parse values
        for item_index, element in enumerate(sorted_contents):
            item_sep = ELBOW if item_index == num_siblings else TEE

            if is_root:
                curr_prefix = ""
            elif current_index == parent_siblings:
                curr_prefix = SPACE
            else:
                curr_prefix = PIPE_SPACE

            new_prefix = prefix + curr_prefix
            if isinstance(element, dict):
                # A dict is a subtree, build the subtree
                _tree += self.build(
                    element,
                    item_index,
                    parent_siblings=num_siblings,
                    prefix=new_prefix,
                    item_sep=item_sep,
                    is_root=False,
                )
            else:
                _tree += f"{new_prefix}{item_sep}{element}\n"
        if is_root:
            return _tree.rstrip()
        return _tree

    def build_tree(self) -> str:
        """Build the tree, without needing to pass in `self.tree`.

        Returns:
            (str): The string containing the directory tree.

        """
        return self.build(self.tree)


class DirTreeBlock(Block):
    """Block Extension for the DirTree"""

    NAME = "dirtree"
    ARGUMENT = None
    OPTIONS = {"type": ["", type_html_identifier]}

    def on_create(self, parent: etree.Element) -> etree.Element:
        """

        Args:
            parent (xml.etree.ElementTree.Element): The parent element in the XML tree.

        Returns:
            (xml.etree.ElementTree.Element): A div container with given classes and
            title text.

        """
        classes = ["admonition"]
        self_type = self.options["type"]
        if self_type:
            classes.append(self_type)
        el = etree.SubElement(parent, "div", {"class": " ".join(classes)})
        title = etree.SubElement(el, "p", {"class": "admonition-title"})
        if not self.argument:
            title.text = "Directory Tree"
        else:
            title.text = self.argument
        return el

    def on_end(self, block: etree.Element) -> None:
        """Inserts the DirTree into the container

        Args:
            block (xml.etree.ElementTree.Element): The block/container created in
            `on_create`
        """
        yaml_content = block.find("p[2]")
        yaml_tree = block.findtext("p[2]")
        if yaml_tree and yaml_content is not None:
            block.remove(yaml_content)
            tree = DirTree(yaml_tree)
            dt = etree.SubElement(block, "pre")
            dt.text = tree.build_tree()


class DirTreeExtension(BlocksExtension):
    """Extension for the DirTree"""

    def extendMarkdownBlocks(
        self, md: markdown.core.Markdown, block_mgr: BlocksProcessor
    ) -> None:
        """Register the `DirTreeBlock` for pymdownx.blocks

        Args:
            md (markdown.core.Markdown): The markdown parser
            block_mgr (BlocksProcessor): The Generic Block Processor
        """
        block_mgr.register(DirTreeBlock, self.getConfigs())


def makeExtension(*args, **kwargs) -> DirTreeExtension:
    """Register the extension with MkDocs.

    Returns:
        (DirTreeExtension): The Directory Tree extension.

    """
    return DirTreeExtension(*args, **kwargs)
