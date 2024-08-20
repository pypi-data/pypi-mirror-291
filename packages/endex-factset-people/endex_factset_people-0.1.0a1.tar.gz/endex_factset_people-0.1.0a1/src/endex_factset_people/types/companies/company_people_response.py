# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CompanyPeopleResponse", "Data"]


class Data(BaseModel):
    email: Optional[str] = None
    """Email of the person"""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Identifier for the company requested."""

    job_function1: Optional[str] = FieldInfo(alias="jobFunction1", default=None)
    """Job Function1"""

    job_function2: Optional[str] = FieldInfo(alias="jobFunction2", default=None)
    """Job Function2"""

    job_function3: Optional[str] = FieldInfo(alias="jobFunction3", default=None)
    """Job Function3"""

    job_function4: Optional[str] = FieldInfo(alias="jobFunction4", default=None)
    """Job Function4"""

    main_phone: Optional[str] = FieldInfo(alias="mainPhone", default=None)
    """Main Phone Numbers of the executives."""

    name: Optional[str] = None
    """FactSet Name of the person"""

    person_id: Optional[str] = FieldInfo(alias="personId", default=None)
    """FactSet Entity Identifier for the Person."""

    phone: Optional[str] = None
    """Phone number of the executives."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Original identifier used for the request."""

    title: Optional[str] = None
    """Executive titles for a specified company."""


class CompanyPeopleResponse(BaseModel):
    data: Optional[List[Data]] = None
