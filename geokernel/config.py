from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AssetsConfig:
    path: Path
    id_column: str = "asset_id"
    type_column: str = "asset_type"


@dataclass(frozen=True)
class TerrainConfig:
    path: Path
    source: str = "local"


@dataclass(frozen=True)
class AnalysisConfig:
    buffer_m: float
    target_crs: str = "EPSG:2154"


@dataclass(frozen=True)
class OutputConfig:
    path: Path


@dataclass(frozen=True)
class GeoKernelConfig:
    assets: AssetsConfig
    terrain: TerrainConfig
    analysis: AnalysisConfig
    output: OutputConfig


def parse_config(raw: dict[str, Any]) -> GeoKernelConfig:
    try:
        return GeoKernelConfig(
            assets=AssetsConfig(
                path=Path(raw["assets"]["path"]),
                id_column=raw["assets"].get("id_column", "asset_id"),
                type_column=raw["assets"].get("type_column", "asset_type"),
            ),
            terrain=TerrainConfig(
                path=Path(raw["terrain"]["path"]),
                source=raw["terrain"].get("source", "local"),
            ),
            analysis=AnalysisConfig(
                buffer_m=float(raw["analysis"]["buffer_m"]),
                target_crs=raw["analysis"].get("target_crs", "EPSG:2154"),
            ),
            output=OutputConfig(
                path=Path(raw["output"]["path"]),
            ),
        )
    except KeyError as exc:
        raise ValueError(f"Missing required config field: {exc}") from exc