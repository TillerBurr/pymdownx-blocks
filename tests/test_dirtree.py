from pymdownx_blocks.dirtree import DirTree, InvalidTreeError, InvalidYAMLError
import pytest
import yaml
import json

root_dir_files = """\
root_dir/:
- file1
- file2"""
expected_root_dir_files = """\
root_dir/
├──file1
└──file2"""

subdir = """\
parent_dir:
- subdir:
    - file1
    - file2"""
expected_subdir = """\
parent_dir
└──subdir
    ├──file1
    └──file2"""

twosub_dir_no_root_files = """\
parent_dir:
- subdir1:
    - file1
    - file2
    - subsubdir:
        - one_file.txt
        - another_file.txt"""

expected_twosub_dir_no_root_files = """\
parent_dir
└──subdir1
    ├──subsubdir
    │   ├──another_file.txt
    │   └──one_file.txt
    ├──file1
    └──file2"""

two_subdir_root_files = """\
parent_dir:
- subdir1:
    - file1
    - file2
    - subsubdir:
        - one_file.txt
        - another_file.txt
- root_file.txt"""

expected_two_subdir_root_files = """\
parent_dir
├──subdir1
│   ├──subsubdir
│   │   ├──another_file.txt
│   │   └──one_file.txt
│   ├──file1
│   └──file2
└──root_file.txt"""

threesubdir = """\
parent_dir:
- subdir:
    - s_file2
    - s_file1
    - subsubdir:
        - subsubsubdir:
            - sss_file.txt
        - subsubsubdir2:
            - sss_file1.txt
            - sss_file2.txt"""
expected_threesubdir = """\
parent_dir
└──subdir
    ├──subsubdir
    │   ├──subsubsubdir
    │   │   └──sss_file.txt
    │   └──subsubsubdir2
    │       ├──sss_file1.txt
    │       └──sss_file2.txt
    ├──s_file1
    └──s_file2"""


@pytest.mark.parametrize(
    "test_input,expected_output",
    [
        (root_dir_files, expected_root_dir_files),
        (subdir, expected_subdir),
        (twosub_dir_no_root_files, expected_twosub_dir_no_root_files),
        (two_subdir_root_files, expected_two_subdir_root_files),
        (threesubdir, expected_threesubdir),
    ],
)
def test_build(test_input, expected_output):
    assert DirTree(test_input).build() == expected_output


def test_invalid_trees():
    multi_root = yaml.dump({"root1": ["file"], "root2": ["file"]})
    with pytest.raises(InvalidTreeError, match="A tree must have a key:value pair"):
        DirTree("test")
    with pytest.raises(
        InvalidTreeError, match="A tree can have only one root directory"
    ):
        DirTree(multi_root)


def test_invalid_yaml():
    bad_dir ="root\n- dir1: file\n- dir2: file2"
    with pytest.raises(InvalidYAMLError):
        DirTree(bad_dir)

