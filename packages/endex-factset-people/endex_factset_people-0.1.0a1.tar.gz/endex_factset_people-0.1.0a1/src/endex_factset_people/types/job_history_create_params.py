# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["JobHistoryCreateParams"]


class JobHistoryCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """FactSet People Entity Ids."""

    level: Literal["SUMMARY", "DETAIL"]
    """Select the level of detail only main Jobs or include other Jobs at a company."""

    status: Literal["ALL", "PRIMARY", "ACTIVE", "INACTIVE"]
    """Select only Jobs with a certain status primary, active, or inactive."""

    type: Literal["ALL", "BRD", "EMP"]
    """Select only Jobs of a certain type board member or employee."""
