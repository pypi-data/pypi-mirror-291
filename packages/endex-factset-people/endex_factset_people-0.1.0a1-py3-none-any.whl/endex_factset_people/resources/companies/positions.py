# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.companies import position_list_params, position_create_params
from ...types.companies.company_positions_response import CompanyPositionsResponse

__all__ = ["PositionsResource", "AsyncPositionsResource"]


class PositionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PositionsResourceWithRawResponse:
        return PositionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PositionsResourceWithStreamingResponse:
        return PositionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
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
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPositionsResponse:
        """
        Returns the list of people, name, and title for a list of company ids and
        requested position. Positions include-

        - Chairman
        - Chief Executive Officer
        - President
        - Chief Operating Officer
        - Chief Financial Officer
        - Chief Technology Officer
        - Chief Investment Officer
        - Founder(s)
        - Compliance Officer
        - Admin
        - Independent Director
        - Directors/Board Members
        - Investor Relations
        - Legal Counsel
        - Treasurer
        - Sales and Marketing Managers
        - Human Resources

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          position: Controls the position details returned for the requested company. By default,
              the service returns the CEO name, title, and ID for the requested company ids.
              |position|description| |---|---| |CHAIR|Chairman| |CEO|Chief Executive Officer|
              |PRES|President| |COO|Chief Operating Officer| |CFO|Chief Financial Officer|
              |CTO|Chief Technology Officer| |CIO|Chief Investment Officer| |FOU|Founder(s)|
              |CMP|Compliance Officer| |ADM|Admin| |IND|Independent Director|
              |BRD|Directors/Board Members| |IR|Investor Relations| |LEG|Legal Counsel|
              |TREAS|Treasurer| |MKT|Sales and Marketing Managers| |HR|Human Resources|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-people/v1/company-positions",
            body=maybe_transform(
                {
                    "ids": ids,
                    "position": position,
                },
                position_create_params.PositionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyPositionsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
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
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPositionsResponse:
        """
        Returns the list of people, name, and title for a list of company ids and
        requested position. Positions include-

        - Chairman
        - Chief Executive Officer
        - President
        - Chief Operating Officer
        - Chief Financial Officer
        - Chief Technology Officer
        - Chief Investment Officer
        - Founder(s)
        - Compliance Officer
        - Admin
        - Independent Director
        - Directors/Board Members
        - Investor Relations
        - Legal Counsel
        - Treasurer
        - Sales and Marketing Managers
        - Human Resources

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          position: Controls the position details returned for the requested company. By default,
              the service returns the CEO name, title, and ID for the requested company ids.
              |position|description| |---|---| |CHAIR|Chairman| |CEO|Chief Executive Officer|
              |PRES|President| |COO|Chief Operating Officer| |CFO|Chief Financial Officer|
              |CTO|Chief Technology Officer| |CIO|Chief Investment Officer| |FOU|Founder(s)|
              |CMP|Compliance Officer| |ADM|Admin| |IND|Independent Director|
              |BRD|Directors/Board Members| |IR|Investor Relations| |LEG|Legal Counsel|
              |TREAS|Treasurer| |MKT|Sales and Marketing Managers| |HR|Human Resources|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-people/v1/company-positions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "position": position,
                    },
                    position_list_params.PositionListParams,
                ),
            ),
            cast_to=CompanyPositionsResponse,
        )


class AsyncPositionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPositionsResourceWithRawResponse:
        return AsyncPositionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPositionsResourceWithStreamingResponse:
        return AsyncPositionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
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
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPositionsResponse:
        """
        Returns the list of people, name, and title for a list of company ids and
        requested position. Positions include-

        - Chairman
        - Chief Executive Officer
        - President
        - Chief Operating Officer
        - Chief Financial Officer
        - Chief Technology Officer
        - Chief Investment Officer
        - Founder(s)
        - Compliance Officer
        - Admin
        - Independent Director
        - Directors/Board Members
        - Investor Relations
        - Legal Counsel
        - Treasurer
        - Sales and Marketing Managers
        - Human Resources

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          position: Controls the position details returned for the requested company. By default,
              the service returns the CEO name, title, and ID for the requested company ids.
              |position|description| |---|---| |CHAIR|Chairman| |CEO|Chief Executive Officer|
              |PRES|President| |COO|Chief Operating Officer| |CFO|Chief Financial Officer|
              |CTO|Chief Technology Officer| |CIO|Chief Investment Officer| |FOU|Founder(s)|
              |CMP|Compliance Officer| |ADM|Admin| |IND|Independent Director|
              |BRD|Directors/Board Members| |IR|Investor Relations| |LEG|Legal Counsel|
              |TREAS|Treasurer| |MKT|Sales and Marketing Managers| |HR|Human Resources|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-people/v1/company-positions",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "position": position,
                },
                position_create_params.PositionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyPositionsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
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
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPositionsResponse:
        """
        Returns the list of people, name, and title for a list of company ids and
        requested position. Positions include-

        - Chairman
        - Chief Executive Officer
        - President
        - Chief Operating Officer
        - Chief Financial Officer
        - Chief Technology Officer
        - Chief Investment Officer
        - Founder(s)
        - Compliance Officer
        - Admin
        - Independent Director
        - Directors/Board Members
        - Investor Relations
        - Legal Counsel
        - Treasurer
        - Sales and Marketing Managers
        - Human Resources

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          position: Controls the position details returned for the requested company. By default,
              the service returns the CEO name, title, and ID for the requested company ids.
              |position|description| |---|---| |CHAIR|Chairman| |CEO|Chief Executive Officer|
              |PRES|President| |COO|Chief Operating Officer| |CFO|Chief Financial Officer|
              |CTO|Chief Technology Officer| |CIO|Chief Investment Officer| |FOU|Founder(s)|
              |CMP|Compliance Officer| |ADM|Admin| |IND|Independent Director|
              |BRD|Directors/Board Members| |IR|Investor Relations| |LEG|Legal Counsel|
              |TREAS|Treasurer| |MKT|Sales and Marketing Managers| |HR|Human Resources|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-people/v1/company-positions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "position": position,
                    },
                    position_list_params.PositionListParams,
                ),
            ),
            cast_to=CompanyPositionsResponse,
        )


class PositionsResourceWithRawResponse:
    def __init__(self, positions: PositionsResource) -> None:
        self._positions = positions

        self.create = to_raw_response_wrapper(
            positions.create,
        )
        self.list = to_raw_response_wrapper(
            positions.list,
        )


class AsyncPositionsResourceWithRawResponse:
    def __init__(self, positions: AsyncPositionsResource) -> None:
        self._positions = positions

        self.create = async_to_raw_response_wrapper(
            positions.create,
        )
        self.list = async_to_raw_response_wrapper(
            positions.list,
        )


class PositionsResourceWithStreamingResponse:
    def __init__(self, positions: PositionsResource) -> None:
        self._positions = positions

        self.create = to_streamed_response_wrapper(
            positions.create,
        )
        self.list = to_streamed_response_wrapper(
            positions.list,
        )


class AsyncPositionsResourceWithStreamingResponse:
    def __init__(self, positions: AsyncPositionsResource) -> None:
        self._positions = positions

        self.create = async_to_streamed_response_wrapper(
            positions.create,
        )
        self.list = async_to_streamed_response_wrapper(
            positions.list,
        )
