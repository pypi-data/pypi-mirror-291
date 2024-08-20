# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["PositionListParams"]


class PositionListParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested company identifier.

    FactSet Identifiers, tickers, CUSIP, SEDOL, and ISIN are accepted inputs.
    <p>**\\**ids limit** = 1000 per request*</p> *<p>Make note, GET Method URL request
    lines are also limited to a total length of 8192 bytes (8KB). In cases where the
    service allows for thousands of ids, which may lead to exceeding this request
    line limit of 8KB, its advised for any requests with large request lines to be
    requested through the respective "POST" method.</p>\\**
    """

    position: Literal[
        "CHAIR",
        "CEO",
        "PRES",
        "COO",
        "CFO",
        "CTO",
        "CIO",
        "FOU",
        "CMP",
        "ADM",
        "IND",
        "BRD",
        "IR",
        "LEG",
        "TREAS",
        "MKT",
        "HR",
    ]
    """Controls the position details returned for the requested company.

    By default, the service returns the CEO name, title, and ID for the requested
    company ids. |position|description| |---|---| |CHAIR|Chairman| |CEO|Chief
    Executive Officer| |PRES|President| |COO|Chief Operating Officer| |CFO|Chief
    Financial Officer| |CTO|Chief Technology Officer| |CIO|Chief Investment Officer|
    |FOU|Founder(s)| |CMP|Compliance Officer| |ADM|Admin| |IND|Independent Director|
    |BRD|Directors/Board Members| |IR|Investor Relations| |LEG|Legal Counsel|
    |TREAS|Treasurer| |MKT|Sales and Marketing Managers| |HR|Human Resources|
    """
