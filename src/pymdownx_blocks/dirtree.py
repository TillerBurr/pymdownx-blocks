from __future__ import annotations
import yaml
from typing import TypeAlias, Union, Sequence
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block
import xml.etree.ElementTree as etree
import markdown


class InvalidYAMLError(BaseException):
    """Raised when YAML is invalid"""


class InvalidTreeError(BaseException):
    """Raised when the YAML is valid, but it not a valid tree"""


PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_SPACE = "│   "
SPACE = "    "

TreeNode: TypeAlias = dict[str, Sequence[Union["TreeNode", str]]]


def sorter(x: Union[TreeNode, str]) -> tuple[bool, str]:
    _type = isinstance(x, str)
    _value = x if isinstance(x, str) else next(iter(x.keys()))
    return _type, _value


class DirTree:
    def __init__(self, in_: str):
        try:
            self.tree = yaml.safe_load(in_)
            if not isinstance(self.tree, dict):
                raise InvalidTreeError("A tree must have a key:value pair")
            if isinstance(self.tree, dict) and len(list(self.tree.keys())) != 1:
                raise InvalidTreeError("A tree can have only one root directory.")
        except yaml.error.YAMLError:
            raise InvalidYAMLError

    def build_output(
        self,
        tree: TreeNode,
        current_index: int = 0,
        prefix: str = "",
        parent_siblings: int = 0,
        item_sep: str = "",
        is_root: bool = True,
    ):
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
                _tree += self.build_output(
                    element,
                    item_index,
                    parent_siblings=num_siblings,
                    prefix=new_prefix,
                    item_sep=item_sep,
                    is_root=False,
                )
            else:
                _tree += f"{new_prefix}{item_sep}{element}\n"
        return _tree

    def build(self) -> str:
        final_tree= self.build_output(self.tree).rstrip()
        return final_tree


class DirTreeBlock(Block):
    NAME = "dirtree"
    ARGUMENT = None
    OPTIONS = {"type": [""]}

    def on_create(self, parent: etree.Element) -> etree.Element:
        return etree.SubElement(parent, "div")

    def on_end(self, block: etree.Element) -> None:
        text = block.findtext("p")
        if text:
            classes = ["admonition"]
            self_type = self.options["type"]
            if self_type:
                classes.append(self_type)

            block.clear()
            tree = DirTree(text)
            el = etree.SubElement(block, "pre", {"class": " ".join(classes)})
            title = etree.SubElement(el, "p", {"class": "admonition-title"})
            if not self.argument:
                title.text = "Directory Tree"
            else:
                title.text = self.argument
            dt = etree.SubElement(el, "p")
            dt.text = tree.build()


class DirTreeExtension(BlocksExtension):
    def extendMarkdownBlocks(
        self, md: markdown.core.Markdown, block_mgr: BlocksProcessor
    ) -> None:
        block_mgr.register(DirTreeBlock, self.getConfigs())


def makeExtension(*args, **kwargs) -> DirTreeExtension:
    return DirTreeExtension(*args, **kwargs)


if __name__ == "__main__":
    tree = DirTree(ex).build()
    print(tree)
