# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import job_history_list_params, job_history_create_params
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
from ..types.people_jobs_response import PeopleJobsResponse

__all__ = ["JobHistoriesResource", "AsyncJobHistoriesResource"]


class JobHistoriesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> JobHistoriesResourceWithRawResponse:
        return JobHistoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> JobHistoriesResourceWithStreamingResponse:
        return JobHistoriesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        level: Literal["SUMMARY", "DETAIL"] | NotGiven = NOT_GIVEN,
        status: Literal["ALL", "PRIMARY", "ACTIVE", "INACTIVE"] | NotGiven = NOT_GIVEN,
        type: Literal["ALL", "BRD", "EMP"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PeopleJobsResponse:
        """
        Returns the `Job` history of the person referenced by the entityId specified in
        the request.

        Args:
          ids: FactSet People Entity Ids.

          level: Select the level of detail only main Jobs or include other Jobs at a company.

          status: Select only Jobs with a certain status primary, active, or inactive.

          type: Select only Jobs of a certain type board member or employee.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-people/v1/jobs",
            body=maybe_transform(
                {
                    "ids": ids,
                    "level": level,
                    "status": status,
                    "type": type,
                },
                job_history_create_params.JobHistoryCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PeopleJobsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        level: Literal["SUMMARY", "DETAIL"] | NotGiven = NOT_GIVEN,
        status: Literal["ALL", "PRIMARY", "ACTIVE", "INACTIVE"] | NotGiven = NOT_GIVEN,
        type: Literal["ALL", "BRD", "EMP"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PeopleJobsResponse:
        """
        Returns the `Job` history of the person referenced by the entityId specified in
        the request.

        Args:
          ids: List of FactSet Person Entity identifier.

          level: Select the level of detail only main Jobs or include other Jobs at a company.

          status: Select only Jobs with a certain status primary, active, or inactive.

          type: Select only Jobs of a certain type board member or employee.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-people/v1/jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "level": level,
                        "status": status,
                        "type": type,
                    },
                    job_history_list_params.JobHistoryListParams,
                ),
            ),
            cast_to=PeopleJobsResponse,
        )


class AsyncJobHistoriesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncJobHistoriesResourceWithRawResponse:
        return AsyncJobHistoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncJobHistoriesResourceWithStreamingResponse:
        return AsyncJobHistoriesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        level: Literal["SUMMARY", "DETAIL"] | NotGiven = NOT_GIVEN,
        status: Literal["ALL", "PRIMARY", "ACTIVE", "INACTIVE"] | NotGiven = NOT_GIVEN,
        type: Literal["ALL", "BRD", "EMP"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PeopleJobsResponse:
        """
        Returns the `Job` history of the person referenced by the entityId specified in
        the request.

        Args:
          ids: FactSet People Entity Ids.

          level: Select the level of detail only main Jobs or include other Jobs at a company.

          status: Select only Jobs with a certain status primary, active, or inactive.

          type: Select only Jobs of a certain type board member or employee.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-people/v1/jobs",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "level": level,
                    "status": status,
                    "type": type,
                },
                job_history_create_params.JobHistoryCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PeopleJobsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        level: Literal["SUMMARY", "DETAIL"] | NotGiven = NOT_GIVEN,
        status: Literal["ALL", "PRIMARY", "ACTIVE", "INACTIVE"] | NotGiven = NOT_GIVEN,
        type: Literal["ALL", "BRD", "EMP"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PeopleJobsResponse:
        """
        Returns the `Job` history of the person referenced by the entityId specified in
        the request.

        Args:
          ids: List of FactSet Person Entity identifier.

          level: Select the level of detail only main Jobs or include other Jobs at a company.

          status: Select only Jobs with a certain status primary, active, or inactive.

          type: Select only Jobs of a certain type board member or employee.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-people/v1/jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "level": level,
                        "status": status,
                        "type": type,
                    },
                    job_history_list_params.JobHistoryListParams,
                ),
            ),
            cast_to=PeopleJobsResponse,
        )


class JobHistoriesResourceWithRawResponse:
    def __init__(self, job_histories: JobHistoriesResource) -> None:
        self._job_histories = job_histories

        self.create = to_raw_response_wrapper(
            job_histories.create,
        )
        self.list = to_raw_response_wrapper(
            job_histories.list,
        )


class AsyncJobHistoriesResourceWithRawResponse:
    def __init__(self, job_histories: AsyncJobHistoriesResource) -> None:
        self._job_histories = job_histories

        self.create = async_to_raw_response_wrapper(
            job_histories.create,
        )
        self.list = async_to_raw_response_wrapper(
            job_histories.list,
        )


class JobHistoriesResourceWithStreamingResponse:
    def __init__(self, job_histories: JobHistoriesResource) -> None:
        self._job_histories = job_histories

        self.create = to_streamed_response_wrapper(
            job_histories.create,
        )
        self.list = to_streamed_response_wrapper(
            job_histories.list,
        )


class AsyncJobHistoriesResourceWithStreamingResponse:
    def __init__(self, job_histories: AsyncJobHistoriesResource) -> None:
        self._job_histories = job_histories

        self.create = async_to_streamed_response_wrapper(
            job_histories.create,
        )
        self.list = async_to_streamed_response_wrapper(
            job_histories.list,
        )
