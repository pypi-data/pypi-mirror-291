# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ExecutiveCreateParams"]


class ExecutiveCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested company identifier.

    FactSet Identifiers, tickers, CUSIP, SEDOL, and ISIN are accepted inputs.
    <p>**\\**ids limit** = 1000 per request*</p> *<p>Make note, GET Method URL request
    lines are also limited to a total length of 8192 bytes (8KB). In cases where the
    service allows for thousands of ids, which may lead to exceeding this request
    line limit of 8KB, its advised for any requests with large request lines to be
    requested through the respective "POST" method.</p>\\**
    """

    function: Literal["PEOPLE", "OFFICER", "DIRECTOR"]
    """Controls the types of people returned based on high-level job functions.

    Filter by - |function|description| |---|---| |PEOPLE|Retrieve **ALL** Executives
    of a requested company| |OFFICER|Retrieve only the Officers of a requested
    company| |DIRECTOR|Retrieve only the Directors of a requested company|
    """
