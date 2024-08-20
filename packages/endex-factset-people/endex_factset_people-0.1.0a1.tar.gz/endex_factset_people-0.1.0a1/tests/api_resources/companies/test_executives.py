# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_people import EndexFactsetPeople, AsyncEndexFactsetPeople
from endex_factset_people.types.companies import CompanyPeopleResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExecutives:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetPeople) -> None:
        executive = client.companies.executives.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetPeople) -> None:
        executive = client.companies.executives.create(
            ids=["AAPL-US"],
            function="PEOPLE",
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetPeople) -> None:
        response = client.companies.executives.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        executive = response.parse()
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetPeople) -> None:
        with client.companies.executives.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            executive = response.parse()
            assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetPeople) -> None:
        executive = client.companies.executives.list(
            ids=["string"],
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetPeople) -> None:
        executive = client.companies.executives.list(
            ids=["string"],
            function="PEOPLE",
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetPeople) -> None:
        response = client.companies.executives.with_raw_response.list(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        executive = response.parse()
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetPeople) -> None:
        with client.companies.executives.with_streaming_response.list(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            executive = response.parse()
            assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncExecutives:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        executive = await async_client.companies.executives.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetPeople) -> None:
        executive = await async_client.companies.executives.create(
            ids=["AAPL-US"],
            function="PEOPLE",
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        response = await async_client.companies.executives.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        executive = await response.parse()
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        async with async_client.companies.executives.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            executive = await response.parse()
            assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetPeople) -> None:
        executive = await async_client.companies.executives.list(
            ids=["string"],
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetPeople) -> None:
        executive = await async_client.companies.executives.list(
            ids=["string"],
            function="PEOPLE",
        )
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetPeople) -> None:
        response = await async_client.companies.executives.with_raw_response.list(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        executive = await response.parse()
        assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetPeople) -> None:
        async with async_client.companies.executives.with_streaming_response.list(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            executive = await response.parse()
            assert_matches_type(CompanyPeopleResponse, executive, path=["response"])

        assert cast(Any, response.is_closed) is True
