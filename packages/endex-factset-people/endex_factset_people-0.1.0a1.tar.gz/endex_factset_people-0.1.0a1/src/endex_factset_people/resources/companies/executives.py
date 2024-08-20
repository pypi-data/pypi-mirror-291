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
from ...types.companies import executive_list_params, executive_create_params
from ...types.companies.company_people_response import CompanyPeopleResponse

__all__ = ["ExecutivesResource", "AsyncExecutivesResource"]


class ExecutivesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExecutivesResourceWithRawResponse:
        return ExecutivesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExecutivesResourceWithStreamingResponse:
        return ExecutivesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        function: Literal["PEOPLE", "OFFICER", "DIRECTOR"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPeopleResponse:
        """
        Returns the list of executives associated the company identifier requested.
        Information includes the job functions, email, phone, title, name, and FactSet
        Entity Identifier. The personId returned can then be used in the /profiles
        endpoint to learn more about the given person.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          function: Controls the types of people returned based on high-level job functions. Filter
              by - |function|description| |---|---| |PEOPLE|Retrieve **ALL** Executives of a
              requested company| |OFFICER|Retrieve only the Officers of a requested company|
              |DIRECTOR|Retrieve only the Directors of a requested company|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-people/v1/company-people",
            body=maybe_transform(
                {
                    "ids": ids,
                    "function": function,
                },
                executive_create_params.ExecutiveCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyPeopleResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        function: Literal["PEOPLE", "OFFICER", "DIRECTOR"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPeopleResponse:
        """
        Returns the list of executives associated the company identifier requested.
        Information includes the job functions, email, phone, title, name, and FactSet
        Entity Identifier. The personId returned can then be used in the `/profiles`
        endpoint to learn more about the given person.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          function: Controls the types of people returned based on high-level job functions. Filter
              by - |function|description| |---|---| |PEOPLE|Retrieve **ALL** Executives of a
              requested company| |OFFICER|Retrieve only the Officers of a requested company|
              |DIRECTOR|Retrieve only the Directors of a requested company|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-people/v1/company-people",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "function": function,
                    },
                    executive_list_params.ExecutiveListParams,
                ),
            ),
            cast_to=CompanyPeopleResponse,
        )


class AsyncExecutivesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExecutivesResourceWithRawResponse:
        return AsyncExecutivesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExecutivesResourceWithStreamingResponse:
        return AsyncExecutivesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        function: Literal["PEOPLE", "OFFICER", "DIRECTOR"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPeopleResponse:
        """
        Returns the list of executives associated the company identifier requested.
        Information includes the job functions, email, phone, title, name, and FactSet
        Entity Identifier. The personId returned can then be used in the /profiles
        endpoint to learn more about the given person.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          function: Controls the types of people returned based on high-level job functions. Filter
              by - |function|description| |---|---| |PEOPLE|Retrieve **ALL** Executives of a
              requested company| |OFFICER|Retrieve only the Officers of a requested company|
              |DIRECTOR|Retrieve only the Directors of a requested company|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-people/v1/company-people",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "function": function,
                },
                executive_create_params.ExecutiveCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyPeopleResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        function: Literal["PEOPLE", "OFFICER", "DIRECTOR"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyPeopleResponse:
        """
        Returns the list of executives associated the company identifier requested.
        Information includes the job functions, email, phone, title, name, and FactSet
        Entity Identifier. The personId returned can then be used in the `/profiles`
        endpoint to learn more about the given person.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          function: Controls the types of people returned based on high-level job functions. Filter
              by - |function|description| |---|---| |PEOPLE|Retrieve **ALL** Executives of a
              requested company| |OFFICER|Retrieve only the Officers of a requested company|
              |DIRECTOR|Retrieve only the Directors of a requested company|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-people/v1/company-people",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "function": function,
                    },
                    executive_list_params.ExecutiveListParams,
                ),
            ),
            cast_to=CompanyPeopleResponse,
        )


class ExecutivesResourceWithRawResponse:
    def __init__(self, executives: ExecutivesResource) -> None:
        self._executives = executives

        self.create = to_raw_response_wrapper(
            executives.create,
        )
        self.list = to_raw_response_wrapper(
            executives.list,
        )


class AsyncExecutivesResourceWithRawResponse:
    def __init__(self, executives: AsyncExecutivesResource) -> None:
        self._executives = executives

        self.create = async_to_raw_response_wrapper(
            executives.create,
        )
        self.list = async_to_raw_response_wrapper(
            executives.list,
        )


class ExecutivesResourceWithStreamingResponse:
    def __init__(self, executives: ExecutivesResource) -> None:
        self._executives = executives

        self.create = to_streamed_response_wrapper(
            executives.create,
        )
        self.list = to_streamed_response_wrapper(
            executives.list,
        )


class AsyncExecutivesResourceWithStreamingResponse:
    def __init__(self, executives: AsyncExecutivesResource) -> None:
        self._executives = executives

        self.create = async_to_streamed_response_wrapper(
            executives.create,
        )
        self.list = async_to_streamed_response_wrapper(
            executives.list,
        )
