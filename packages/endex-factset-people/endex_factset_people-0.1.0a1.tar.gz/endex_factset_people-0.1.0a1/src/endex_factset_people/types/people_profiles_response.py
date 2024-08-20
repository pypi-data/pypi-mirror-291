# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["PeopleProfilesResponse", "Data"]


class Data(BaseModel):
    age: Optional[float] = None
    """Person's age in years."""

    biography: Optional[str] = None
    """Brief biography of the person requested."""

    factset_name: Optional[str] = FieldInfo(alias="factsetName", default=None)
    """Name"""

    first_name: Optional[str] = FieldInfo(alias="firstName", default=None)
    """First Name"""

    formal_name: Optional[str] = FieldInfo(alias="formalName", default=None)
    """Formal Name"""

    gender: Optional[str] = None
    """Person's Gender."""

    highest_degree: Optional[str] = FieldInfo(alias="highestDegree", default=None)
    """The Highest Held Degree Code."""

    highest_degree_inst: Optional[str] = FieldInfo(alias="highestDegreeInst", default=None)
    """The Highest Degree Institution Name."""

    last_name: Optional[str] = FieldInfo(alias="lastName", default=None)
    """Last Name"""

    middle_name: Optional[str] = FieldInfo(alias="middleName", default=None)
    """Middle Name"""

    person_id: Optional[str] = FieldInfo(alias="personId", default=None)
    """FactSet Entity Identifier for the Person"""

    primary_company_id: Optional[str] = FieldInfo(alias="primaryCompanyId", default=None)
    """Entity identifier of primary `Company` of employment."""

    primary_company_name: Optional[str] = FieldInfo(alias="primaryCompanyName", default=None)
    """Name of primary company of employment"""

    primary_title: Optional[str] = FieldInfo(alias="primaryTitle", default=None)
    """Title at primary `Company` of employment"""

    proper_name: Optional[str] = FieldInfo(alias="properName", default=None)
    """Proper Name"""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Person identifier used in the request."""

    salary: Optional[float] = None
    """Most Recent Salary"""

    salutation: Optional[str] = None
    """Primary Salutation of Name"""

    suffix: Optional[str] = None
    """Suffix of Name"""

    total_compensation: Optional[float] = FieldInfo(alias="totalCompensation", default=None)
    """Most Recent Total Compensation"""


class PeopleProfilesResponse(BaseModel):
    data: Optional[List[Data]] = None
