# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

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
from ...types.companies import compensation_list_params, compensation_create_params
from ...types.companies.company_compensation_response import CompanyCompensationResponse

__all__ = ["CompensationsResource", "AsyncCompensationsResource"]


class CompensationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompensationsResourceWithRawResponse:
        return CompensationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompensationsResourceWithStreamingResponse:
        return CompensationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyCompensationResponse:
        """
        Returns the list of company-level executive compensation data items for the top
        executives listed in annual filings for the most recent fiscal year. The
        coverage of the compensation details for the executives are limited to US
        region. All the compensation figures are expressed in raw units.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-people/v1/company-compensation",
            body=maybe_transform({"ids": ids}, compensation_create_params.CompensationCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyCompensationResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyCompensationResponse:
        """
        Returns the list of company-level executive compensation data items for the top
        executives listed in annual filings.The coverage of the compensation details for
        the executives are limited to US region. All the compensation figures are
        expressed in raw units.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-people/v1/company-compensation",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, compensation_list_params.CompensationListParams),
            ),
            cast_to=CompanyCompensationResponse,
        )


class AsyncCompensationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompensationsResourceWithRawResponse:
        return AsyncCompensationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompensationsResourceWithStreamingResponse:
        return AsyncCompensationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyCompensationResponse:
        """
        Returns the list of company-level executive compensation data items for the top
        executives listed in annual filings for the most recent fiscal year. The
        coverage of the compensation details for the executives are limited to US
        region. All the compensation figures are expressed in raw units.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-people/v1/company-compensation",
            body=await async_maybe_transform({"ids": ids}, compensation_create_params.CompensationCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyCompensationResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyCompensationResponse:
        """
        Returns the list of company-level executive compensation data items for the top
        executives listed in annual filings.The coverage of the compensation details for
        the executives are limited to US region. All the compensation figures are
        expressed in raw units.

        Args:
          ids: The requested company identifier. FactSet Identifiers, tickers, CUSIP, SEDOL,
              and ISIN are accepted inputs. <p>**\\**ids limit** = 1000 per request*</p>
              *<p>Make note, GET Method URL request lines are also limited to a total length
              of 8192 bytes (8KB). In cases where the service allows for thousands of ids,
              which may lead to exceeding this request line limit of 8KB, its advised for any
              requests with large request lines to be requested through the respective "POST"
              method.</p>\\**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-people/v1/company-compensation",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, compensation_list_params.CompensationListParams),
            ),
            cast_to=CompanyCompensationResponse,
        )


class CompensationsResourceWithRawResponse:
    def __init__(self, compensations: CompensationsResource) -> None:
        self._compensations = compensations

        self.create = to_raw_response_wrapper(
            compensations.create,
        )
        self.list = to_raw_response_wrapper(
            compensations.list,
        )


class AsyncCompensationsResourceWithRawResponse:
    def __init__(self, compensations: AsyncCompensationsResource) -> None:
        self._compensations = compensations

        self.create = async_to_raw_response_wrapper(
            compensations.create,
        )
        self.list = async_to_raw_response_wrapper(
            compensations.list,
        )


class CompensationsResourceWithStreamingResponse:
    def __init__(self, compensations: CompensationsResource) -> None:
        self._compensations = compensations

        self.create = to_streamed_response_wrapper(
            compensations.create,
        )
        self.list = to_streamed_response_wrapper(
            compensations.list,
        )


class AsyncCompensationsResourceWithStreamingResponse:
    def __init__(self, compensations: AsyncCompensationsResource) -> None:
        self._compensations = compensations

        self.create = async_to_streamed_response_wrapper(
            compensations.create,
        )
        self.list = async_to_streamed_response_wrapper(
            compensations.list,
        )
