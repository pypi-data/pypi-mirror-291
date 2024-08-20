# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CompanyPositionsResponse", "Data"]


class Data(BaseModel):
    age: Optional[float] = None
    """The age of the person requested."""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Identifier for the company."""

    gender: Optional[str] = None
    """The Gender of the person requested."""

    name: Optional[str] = None
    """FactSet Name of the person"""

    person_id: Optional[str] = FieldInfo(alias="personId", default=None)
    """Factset Entity Identifier for the Person"""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Original identifier used for the request."""

    request_position: Optional[str] = FieldInfo(alias="requestPosition", default=None)
    """The requested position code."""

    title: Optional[str] = None
    """The requested Position Title"""

    years_at_firm: Optional[float] = FieldInfo(alias="yearsAtFirm", default=None)
    """The number of years individual is at firm.

    For founders, this is since inception.
    """


class CompanyPositionsResponse(BaseModel):
    data: Optional[List[Data]] = None
