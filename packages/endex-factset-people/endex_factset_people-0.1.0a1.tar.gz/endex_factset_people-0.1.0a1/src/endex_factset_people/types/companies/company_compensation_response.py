# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CompanyCompensationResponse", "Data"]


class Data(BaseModel):
    bonus: Optional[float] = None
    """Bonus of the executive during the fiscal year. Expressed in USD and raw units."""

    compensation_year: Optional[str] = FieldInfo(alias="compensationYear", default=None)
    """
    The most recent year of compensation is expressed as 'YYYY' as opposed to
    'YYYY-MM-DD' format.
    """

    name: Optional[str] = None
    """FactSet Name of the person"""

    non_equity_incentive_plan_comp: Optional[float] = FieldInfo(alias="nonEquityIncentivePlanComp", default=None)
    """All the earnings pursuant to awards under non-equity incentive plans.

    Expressed in USD and raw units.
    """

    non_qualified_comp_earnings: Optional[float] = FieldInfo(alias="nonQualifiedCompEarnings", default=None)
    """
    All the other nonqualified defined contribution which are not tax qualified and
    other contributions. Expressed in USD and raw units.
    """

    options_awards: Optional[float] = FieldInfo(alias="optionsAwards", default=None)
    """Option Awards for the person. Expressed in USD and raw units."""

    other_compensation: Optional[float] = FieldInfo(alias="otherCompensation", default=None)
    """
    All the other compensations which are not explicitly defined as salary, bonus,
    stock awards, or options awards. Expressed in USD and raw units.
    """

    person_id: Optional[str] = FieldInfo(alias="personId", default=None)
    """Factset Entity Identifier for the Person"""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Original identifier used for the request."""

    salary: Optional[float] = None
    """Salary of the person. Expressed in USD and raw units."""

    stock_awards: Optional[float] = FieldInfo(alias="stockAwards", default=None)
    """Stock awards for the person. Expressed in USD and raw units."""

    title: Optional[str] = None
    """The requested Position Title"""

    total_compensation: Optional[float] = FieldInfo(alias="totalCompensation", default=None)
    """The sum of all compensation for the requested person as reported by the company.

    Expressed in USD and raw units.
    """


class CompanyCompensationResponse(BaseModel):
    data: Optional[List[Data]] = None
