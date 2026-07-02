from pathlib import Path

import pytest

from geokernel.io import load_config


def test_load_config_valid_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
        assets:
        path: data/sample/roads.geojson
        terrain:
        path: data/sample/dem.tif
        output:
        path: data/outputs/features.geoparquet
        """,
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config["assets"]["path"] == "data/sample/roads_clean.geojson"
    assert config["terrain"]["path"] == "data/sample/dem.tif"


def test_load_config_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        load_config("missing.yaml")


def test_load_config_rejects_non_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "config.txt"
    config_path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError):
        load_config(config_path)