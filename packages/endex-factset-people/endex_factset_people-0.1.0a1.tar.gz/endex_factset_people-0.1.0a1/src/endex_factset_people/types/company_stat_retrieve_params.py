# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CompanyStatRetrieveParams"]


class CompanyStatRetrieveParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested company identifier.

    FactSet Identifiers, tickers, CUSIP, SEDOL, and ISIN are accepted inputs.
    <p>**\\**ids limit** = 1000 per request*</p> *<p>Make note, GET Method URL request
    lines are also limited to a total length of 8192 bytes (8KB). In cases where the
    service allows for thousands of ids, which may lead to exceeding this request
    line limit of 8KB, its advised for any requests with large request lines to be
    requested through the respective "POST" method.</p>\\**
    """

    mb_type: Annotated[Literal["MB", "MGMT", "BRD"], PropertyInfo(alias="mbType")]
    """Search based on the management and board types.

    The types include - |type|description| |---|---| |MB|Management & Board|
    |MGMT|Management| |BRD|Board|
    """
