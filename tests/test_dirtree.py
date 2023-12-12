import pytest
import yaml
from pymdownx_blocks.dirtree import DirTree, InvalidTreeError, InvalidYAMLError

from tests.utils import dedent, dedent_and_replace
root_dir_files = """
                 root_dir/:
                    - file1
                    - file2
                 """
expected_root_dir_files = """
                          root_dir/
                          ├──file1
                          └──file2
                          """

subdir = """
         parent_dir:
         - subdir:
             - file1
             - file2
         """
expected_subdir = """
                  parent_dir
                  └──subdir
                      ├──file1
                      └──file2
                  """

twosub_dir_no_root_files = """
                           parent_dir:
                           - subdir1:
                               - file1
                               - file2
                               - subsubdir:
                                   - one_file.txt
                                   - another_file.txt
                           """

expected_twosub_dir_no_root_files = """
                                    parent_dir
                                    └──subdir1
                                        ├──subsubdir
                                        │   ├──another_file.txt
                                        │   └──one_file.txt
                                        ├──file1
                                        └──file2
                                    """

two_subdir_root_files = """
                        parent_dir:
                        - subdir1:
                            - file1
                            - file2
                            - subsubdir:
                                - one_file.txt
                                - another_file.txt
                        - root_file.txt
                        """

expected_two_subdir_root_files = """
                                 parent_dir
                                 ├──subdir1
                                 │   ├──subsubdir
                                 │   │   ├──another_file.txt
                                 │   │   └──one_file.txt
                                 │   ├──file1
                                 │   └──file2
                                 └──root_file.txt
                                 """

threesubdir = """
              parent_dir:
              - subdir:
                  - s_file2
                  - s_file1
                  - subsubdir:
                      - subsubsubdir:
                          - sss_file.txt
                      - subsubsubdir2:
                          - sss_file1.txt
                          - sss_file2.txt
              """
expected_threesubdir = """
                       parent_dir
                       └──subdir
                           ├──subsubdir
                           │   ├──subsubsubdir
                           │   │   └──sss_file.txt
                           │   └──subsubsubdir2
                           │       ├──sss_file1.txt
                           │       └──sss_file2.txt
                           ├──s_file1
                           └──s_file2
                       """


def generate_dirtree_input(
    placeholder: str, title: str | None = None, _type: str | None = None
):
    if title is None:
        title = ""
    else:
        title = f" | {title}"
    if _type is None:
        _type = ""
    else:
        _type = f"type: {_type}"

    _input = f"""
        /// dirtree{title}
            {_type}

        {placeholder}
        ///
        """
    return dedent(_input)


def generate_dirtree_expected(
    placeholder: str, title: str | None = None, _type: str | None = None
):
    if title is None:
        title = "Directory Tree"
    if _type is None:
        _type = ""
    else:
        _type = f" {_type}"
    expected = f"""
               <div class="admonition{_type}">
               <p class="admonition-title">{title}</p>
               <pre>{placeholder}</pre>
               </div>
               """
    return dedent(expected)


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
    dedent_in = dedent(test_input)
    dedent_out = dedent(expected_output)
    assert DirTree(dedent_in).build() == dedent_out


def test_invalid_trees():
    multi_root = yaml.dump({"root1": ["file"], "root2": ["file"]})
    with pytest.raises(InvalidTreeError, match="A tree must have a key:value pair"):
        DirTree("test")
    with pytest.raises(
        InvalidTreeError, match="A tree can have only one root directory"
    ):
        DirTree(multi_root)


def test_invalid_yaml():
    bad_dir = "root\n- dir1: file\n- dir2: file2"
    with pytest.raises(InvalidYAMLError):
        DirTree(bad_dir)


@pytest.mark.parametrize("class_type", ["note", "warning", "tip", "danger", None])
@pytest.mark.parametrize("title", ["A Title", "AnotherTitle",None])
def test_title(markdown_fixture, class_type, title):
    md = markdown_fixture(
        ["pymdownx_blocks.dirtree"], extension_config={"pymdownx_blocks.dirtree": []}
    )
    placeholder = "{{DIRTREE}}"
    _input = generate_dirtree_input(placeholder, title=title, _type=class_type)
    _input = dedent_and_replace(_input, placeholder, threesubdir, dedent_new=True)

    expected = generate_dirtree_expected(placeholder, title=title, _type=class_type)
    expected = dedent_and_replace(
        expected, placeholder, expected_threesubdir, dedent_new=True
    )

    results = md.convert(_input)
    assert results == expected
