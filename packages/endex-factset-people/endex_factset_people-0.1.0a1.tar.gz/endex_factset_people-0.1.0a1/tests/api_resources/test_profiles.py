# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_people import EndexFactsetPeople, AsyncEndexFactsetPeople
from endex_factset_people.types import PeopleProfilesResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProfiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetPeople) -> None:
        profile = client.profiles.create(
            ids=["0DPHLH-E"],
        )
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetPeople) -> None:
        response = client.profiles.with_raw_response.create(
            ids=["0DPHLH-E"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetPeople) -> None:
        with client.profiles.with_streaming_response.create(
            ids=["0DPHLH-E"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetPeople) -> None:
        profile = client.profiles.list(
            ids=["string"],
        )
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetPeople) -> None:
        response = client.profiles.with_raw_response.list(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetPeople) -> None:
        with client.profiles.with_streaming_response.list(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncProfiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        profile = await async_client.profiles.create(
            ids=["0DPHLH-E"],
        )
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        response = await async_client.profiles.with_raw_response.create(
            ids=["0DPHLH-E"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetPeople) -> None:
        async with async_client.profiles.with_streaming_response.create(
            ids=["0DPHLH-E"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetPeople) -> None:
        profile = await async_client.profiles.list(
            ids=["string"],
        )
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetPeople) -> None:
        response = await async_client.profiles.with_raw_response.list(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetPeople) -> None:
        async with async_client.profiles.with_streaming_response.list(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(PeopleProfilesResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True
