# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import company_stat_create_params, company_stat_retrieve_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.company_stats_response import CompanyStatsResponse

__all__ = ["CompanyStatsResource", "AsyncCompanyStatsResource"]


class CompanyStatsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompanyStatsResourceWithRawResponse:
        return CompanyStatsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompanyStatsResourceWithStreamingResponse:
        return CompanyStatsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        mb_type: Literal["MB", "MGMT", "BRD"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyStatsResponse:
        """
        Returns the statistics such as the average age, tenure, compensation of
        leadership, number of executives, and the gender diversity of leadership. We can
        utilize the data for analyzing a company's board and management.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          mb_type: Search based on the management and board types. The types include -
              |type|description| |---|---| |MB|Management & Board| |MGMT|Management|
              |BRD|Board|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-people/v1/company-stats",
            body=maybe_transform(
                {
                    "ids": ids,
                    "mb_type": mb_type,
                },
                company_stat_create_params.CompanyStatCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyStatsResponse,
        )

    def retrieve(
        self,
        *,
        ids: List[str],
        mb_type: Literal["MB", "MGMT", "BRD"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyStatsResponse:
        """
        Returns the statistics such as the average age, tenure, compensation of
        leadership, number of executives, and the gender diversity of leadership. We can
        utilize the data for analyzing a company's board and management.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          mb_type: Search based on the management and board types. The types include -
              |type|description| |---|---| |MB|Management & Board| |MGMT|Management|
              |BRD|Board|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-people/v1/company-stats",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "mb_type": mb_type,
                    },
                    company_stat_retrieve_params.CompanyStatRetrieveParams,
                ),
            ),
            cast_to=CompanyStatsResponse,
        )


class AsyncCompanyStatsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompanyStatsResourceWithRawResponse:
        return AsyncCompanyStatsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompanyStatsResourceWithStreamingResponse:
        return AsyncCompanyStatsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        mb_type: Literal["MB", "MGMT", "BRD"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyStatsResponse:
        """
        Returns the statistics such as the average age, tenure, compensation of
        leadership, number of executives, and the gender diversity of leadership. We can
        utilize the data for analyzing a company's board and management.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          mb_type: Search based on the management and board types. The types include -
              |type|description| |---|---| |MB|Management & Board| |MGMT|Management|
              |BRD|Board|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-people/v1/company-stats",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "mb_type": mb_type,
                },
                company_stat_create_params.CompanyStatCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyStatsResponse,
        )

    async def retrieve(
        self,
        *,
        ids: List[str],
        mb_type: Literal["MB", "MGMT", "BRD"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyStatsResponse:
        """
        Returns the statistics such as the average age, tenure, compensation of
        leadership, number of executives, and the gender diversity of leadership. We can
        utilize the data for analyzing a company's board and management.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          mb_type: Search based on the management and board types. The types include -
              |type|description| |---|---| |MB|Management & Board| |MGMT|Management|
              |BRD|Board|

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-people/v1/company-stats",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "mb_type": mb_type,
                    },
                    company_stat_retrieve_params.CompanyStatRetrieveParams,
                ),
            ),
            cast_to=CompanyStatsResponse,
        )


class CompanyStatsResourceWithRawResponse:
    def __init__(self, company_stats: CompanyStatsResource) -> None:
        self._company_stats = company_stats

        self.create = to_raw_response_wrapper(
            company_stats.create,
        )
        self.retrieve = to_raw_response_wrapper(
            company_stats.retrieve,
        )


class AsyncCompanyStatsResourceWithRawResponse:
    def __init__(self, company_stats: AsyncCompanyStatsResource) -> None:
        self._company_stats = company_stats

        self.create = async_to_raw_response_wrapper(
            company_stats.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            company_stats.retrieve,
        )


class CompanyStatsResourceWithStreamingResponse:
    def __init__(self, company_stats: CompanyStatsResource) -> None:
        self._company_stats = company_stats

        self.create = to_streamed_response_wrapper(
            company_stats.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            company_stats.retrieve,
        )


class AsyncCompanyStatsResourceWithStreamingResponse:
    def __init__(self, company_stats: AsyncCompanyStatsResource) -> None:
        self._company_stats = company_stats

        self.create = async_to_streamed_response_wrapper(
            company_stats.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            company_stats.retrieve,
        )
