# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from .positions import (
    PositionsResource,
    AsyncPositionsResource,
    PositionsResourceWithRawResponse,
    AsyncPositionsResourceWithRawResponse,
    PositionsResourceWithStreamingResponse,
    AsyncPositionsResourceWithStreamingResponse,
)
from .executives import (
    ExecutivesResource,
    AsyncExecutivesResource,
    ExecutivesResourceWithRawResponse,
    AsyncExecutivesResourceWithRawResponse,
    ExecutivesResourceWithStreamingResponse,
    AsyncExecutivesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .compensations import (
    CompensationsResource,
    AsyncCompensationsResource,
    CompensationsResourceWithRawResponse,
    AsyncCompensationsResourceWithRawResponse,
    CompensationsResourceWithStreamingResponse,
    AsyncCompensationsResourceWithStreamingResponse,
)

__all__ = ["CompaniesResource", "AsyncCompaniesResource"]


class CompaniesResource(SyncAPIResource):
    @cached_property
    def executives(self) -> ExecutivesResource:
        return ExecutivesResource(self._client)

    @cached_property
    def positions(self) -> PositionsResource:
        return PositionsResource(self._client)

    @cached_property
    def compensations(self) -> CompensationsResource:
        return CompensationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> CompaniesResourceWithRawResponse:
        return CompaniesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompaniesResourceWithStreamingResponse:
        return CompaniesResourceWithStreamingResponse(self)


class AsyncCompaniesResource(AsyncAPIResource):
    @cached_property
    def executives(self) -> AsyncExecutivesResource:
        return AsyncExecutivesResource(self._client)

    @cached_property
    def positions(self) -> AsyncPositionsResource:
        return AsyncPositionsResource(self._client)

    @cached_property
    def compensations(self) -> AsyncCompensationsResource:
        return AsyncCompensationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCompaniesResourceWithRawResponse:
        return AsyncCompaniesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompaniesResourceWithStreamingResponse:
        return AsyncCompaniesResourceWithStreamingResponse(self)


class CompaniesResourceWithRawResponse:
    def __init__(self, companies: CompaniesResource) -> None:
        self._companies = companies

    @cached_property
    def executives(self) -> ExecutivesResourceWithRawResponse:
        return ExecutivesResourceWithRawResponse(self._companies.executives)

    @cached_property
    def positions(self) -> PositionsResourceWithRawResponse:
        return PositionsResourceWithRawResponse(self._companies.positions)

    @cached_property
    def compensations(self) -> CompensationsResourceWithRawResponse:
        return CompensationsResourceWithRawResponse(self._companies.compensations)


class AsyncCompaniesResourceWithRawResponse:
    def __init__(self, companies: AsyncCompaniesResource) -> None:
        self._companies = companies

    @cached_property
    def executives(self) -> AsyncExecutivesResourceWithRawResponse:
        return AsyncExecutivesResourceWithRawResponse(self._companies.executives)

    @cached_property
    def positions(self) -> AsyncPositionsResourceWithRawResponse:
        return AsyncPositionsResourceWithRawResponse(self._companies.positions)

    @cached_property
    def compensations(self) -> AsyncCompensationsResourceWithRawResponse:
        return AsyncCompensationsResourceWithRawResponse(self._companies.compensations)


class CompaniesResourceWithStreamingResponse:
    def __init__(self, companies: CompaniesResource) -> None:
        self._companies = companies

    @cached_property
    def executives(self) -> ExecutivesResourceWithStreamingResponse:
        return ExecutivesResourceWithStreamingResponse(self._companies.executives)

    @cached_property
    def positions(self) -> PositionsResourceWithStreamingResponse:
        return PositionsResourceWithStreamingResponse(self._companies.positions)

    @cached_property
    def compensations(self) -> CompensationsResourceWithStreamingResponse:
        return CompensationsResourceWithStreamingResponse(self._companies.compensations)


class AsyncCompaniesResourceWithStreamingResponse:
    def __init__(self, companies: AsyncCompaniesResource) -> None:
        self._companies = companies

    @cached_property
    def executives(self) -> AsyncExecutivesResourceWithStreamingResponse:
        return AsyncExecutivesResourceWithStreamingResponse(self._companies.executives)

    @cached_property
    def positions(self) -> AsyncPositionsResourceWithStreamingResponse:
        return AsyncPositionsResourceWithStreamingResponse(self._companies.positions)

    @cached_property
    def compensations(self) -> AsyncCompensationsResourceWithStreamingResponse:
        return AsyncCompensationsResourceWithStreamingResponse(self._companies.compensations)
