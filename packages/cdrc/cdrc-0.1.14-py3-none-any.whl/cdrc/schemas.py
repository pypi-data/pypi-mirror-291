from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class FeatureTypes(Enum):
    LEGEND_ITEM = "legend_item"
    POLYGON = "polygon"
    LINE = "line"
    POINT = "point"
    AREA_EXTRACTION = "area_extraction"


class FeatureSearchByCog(BaseModel):
    feature_types: List[FeatureTypes] = Field(default_factory=list, description="List of features to return")
    system_versions: Optional[List[tuple]] = Field(
        default_factory=list, description="List of system and system version pairs"
    )
    search_text: str = Field(default="", description="String text to search for in legend descriptions")
    validated: Optional[bool] = None
    legend_ids: Optional[List[str]] = Field(
        default_factory=list, description="List of legend ids to filter on if known"
    )
    georeferenced_data: bool = Field(default=False, description="Return georeferenced values")
    page: int = Field(description="Page", default=0)
    size: int = Field(description="Number of results", default=10)


class Polygon(BaseModel):
    """
    Individual polygon segmentation of a polygon feature.
    """

    coordinates: List[List[List[Union[float, int]]]] = Field(
        description="""The coordinates of the polygon. Format is expected to
                    be [x,y] coordinate pairs where the top left is the origin
                    (0,0)."""
    )
    type: str = "Polygon"


class FeatureSearch(BaseModel):
    cog_ids: Optional[List[str]] = Field(default_factory=list, description="List of cog ids to filter on if known")
    category: str = Field(default="", description="Feature category")
    system_versions: Optional[List[tuple]] = Field(
        default_factory=list, description="List of system and system version pairs"
    )
    search_text: Optional[str] = Field(default=None, description="String text to search for in legend descriptions")
    validated: Optional[bool] = True
    legend_ids: Optional[List[str]] = Field(
        default_factory=list, description="List of legend ids to filter on if known"
    )
    georeferenced_data: bool = Field(default=False, description="Return georeferenced values")
    page: int = Field(description="Page", default=0)
    size: int = Field(description="Number of results", default=10)


class FeatureSearchIntersect(FeatureSearch):
    intersect_polygon: Optional[Polygon] = Field(default=None, description="Polygon geojson")
