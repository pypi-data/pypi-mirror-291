# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CompanyStatsResponse", "Data"]


class Data(BaseModel):
    average_age: Optional[float] = FieldInfo(alias="averageAge", default=None)
    """Average of the executives on the management and board"""

    average_mgmt_compensation: Optional[float] = FieldInfo(alias="averageMgmtCompensation", default=None)
    """Average compensation for the executives"""

    average_tenure: Optional[float] = FieldInfo(alias="averageTenure", default=None)
    """Avergae tenure of the people"""

    board_independent_directors: Optional[float] = FieldInfo(alias="boardIndependentDirectors", default=None)
    """Independent directors on the board"""

    female_board_members: Optional[float] = FieldInfo(alias="femaleBoardMembers", default=None)
    """Number of female members on the board"""

    female_board_members_percent: Optional[float] = FieldInfo(alias="femaleBoardMembersPercent", default=None)
    """Percentage of female members on the board"""

    max_age: Optional[float] = FieldInfo(alias="maxAge", default=None)
    """Maximum age of the people on Management & Board"""

    mb_type: Optional[str] = FieldInfo(alias="mbType", default=None)
    """
    Management and Board type, where MB = Management & Board, MGMT = Management, and
    BRD = Board. This is a pass-through value from the input used in the `mbType`
    query parameter.
    """

    median_age: Optional[float] = FieldInfo(alias="medianAge", default=None)
    """Median age of the people on board"""

    median_tenure: Optional[float] = FieldInfo(alias="medianTenure", default=None)
    """Median tenure"""

    minimum_age: Optional[float] = FieldInfo(alias="minimumAge", default=None)
    """Minimum age of the person on board"""

    number_of_members: Optional[float] = FieldInfo(alias="numberOfMembers", default=None)
    """Number of people on board."""

    on_other_boards_all: Optional[float] = FieldInfo(alias="onOtherBoardsAll", default=None)
    """On Other Boards All"""

    on_other_boards_corporate: Optional[float] = FieldInfo(alias="onOtherBoardsCorporate", default=None)
    """On Other Boards Corporate"""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Original identifier used for the request."""


class CompanyStatsResponse(BaseModel):
    data: Optional[List[Data]] = None
