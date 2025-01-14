import os

from trlx.data.configs import TRLConfig
from typing import List


def _get_config_dirs(dir: str, config_dir_name: str = "configs") -> List[str]:
    """Returns all sub-directories of `dir` named `configs`."""
    config_dirs = []
    for root, dirs, _ in os.walk(dir):
        config_dirs.extend(os.path.join(root, d) for d in dirs if d == config_dir_name)
    return config_dirs


def _get_yaml_filepaths(dir: str) -> List[str]:
    """Returns a list of `yml` filepaths in `dir`."""
    return [
        os.path.join(dir, file)
        for file in os.listdir(dir)
        if file.endswith(".yml")
    ]


def test_repo_trl_configs():
    """Tests to ensure all default configs in the repository are valid."""
    config_dirs = ["configs", *_get_config_dirs("examples")]
    config_files = sum(map(_get_yaml_filepaths, config_dirs), [])  # sum for flat-map behavior
    for file in config_files:
        assert os.path.isfile(file), f"Config file {file} does not exist."
        assert file.endswith(".yml"), f"Config file {file} is not a yaml file."
        try:
            TRLConfig.load_yaml(file)
        except Exception as e:
            assert False, f"Failed to load config file `{file}` with error `{e}`"
