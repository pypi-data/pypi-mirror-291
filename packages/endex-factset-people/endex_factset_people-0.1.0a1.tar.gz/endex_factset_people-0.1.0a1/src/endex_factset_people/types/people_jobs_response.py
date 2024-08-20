# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["PeopleJobsResponse", "Data"]


class Data(BaseModel):
    company_city: Optional[str] = FieldInfo(alias="companyCity", default=None)
    """City the job is located in."""

    company_id: Optional[str] = FieldInfo(alias="companyId", default=None)
    """FactSet Identifier for the company."""

    company_name: Optional[str] = FieldInfo(alias="companyName", default=None)
    """Name of the company."""

    job_end_date: Optional[date] = FieldInfo(alias="jobEndDate", default=None)
    """Ending date for the Job."""

    job_function_code: Optional[str] = FieldInfo(alias="jobFunctionCode", default=None)
    """Job function code."""

    job_function_name: Optional[str] = FieldInfo(alias="jobFunctionName", default=None)
    """Description of the job."""

    job_start_date: Optional[date] = FieldInfo(alias="jobStartDate", default=None)
    """Starting date for the Job."""

    job_title: Optional[str] = FieldInfo(alias="jobTitle", default=None)
    """Job Title"""

    person_id: Optional[str] = FieldInfo(alias="personId", default=None)
    """FactSet Entity Identifier for the Person."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Original identifier used for the request."""


class PeopleJobsResponse(BaseModel):
    data: Optional[List[Data]] = None
