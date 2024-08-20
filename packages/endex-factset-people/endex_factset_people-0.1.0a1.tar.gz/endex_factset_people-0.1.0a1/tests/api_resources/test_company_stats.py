# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_people import EndexFactsetPeople, AsyncEndexFactsetPeople
from endex_factset_people.types import CompanyStatsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompanyStats:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetPeople) -> None:
        company_stat = client.company_stats.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetPeople) -> None:
        company_stat = client.company_stats.create(
            ids=["AAPL-US"],
            mb_type="MB",
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetPeople) -> None:
        response = client.company_stats.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company_stat = response.parse()
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetPeople) -> None:
        with client.company_stats.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company_stat = response.parse()
            assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetPeople) -> None:
        company_stat = client.company_stats.retrieve(
            ids=["string"],
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetPeople) -> None:
        company_stat = client.company_stats.retrieve(
            ids=["string"],
            mb_type="MB",
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetPeople) -> None:
        response = client.company_stats.with_raw_response.retrieve(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company_stat = response.parse()
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetPeople) -> None:
        with client.company_stats.with_streaming_response.retrieve(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company_stat = response.parse()
            assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCompanyStats:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        company_stat = await async_client.company_stats.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetPeople) -> None:
        company_stat = await async_client.company_stats.create(
            ids=["AAPL-US"],
            mb_type="MB",
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        response = await async_client.company_stats.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company_stat = await response.parse()
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        async with async_client.company_stats.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company_stat = await response.parse()
            assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetPeople) -> None:
        company_stat = await async_client.company_stats.retrieve(
            ids=["string"],
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetPeople) -> None:
        company_stat = await async_client.company_stats.retrieve(
            ids=["string"],
            mb_type="MB",
        )
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetPeople) -> None:
        response = await async_client.company_stats.with_raw_response.retrieve(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        company_stat = await response.parse()
        assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetPeople) -> None:
        async with async_client.company_stats.with_streaming_response.retrieve(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            company_stat = await response.parse()
            assert_matches_type(CompanyStatsResponse, company_stat, path=["response"])

        assert cast(Any, response.is_closed) is True
