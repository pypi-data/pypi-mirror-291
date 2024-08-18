# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bdnb_api import BdnbAPI, AsyncBdnbAPI
from tests.utils import assert_matches_type
from bdnb_api.pagination import SyncDefault, AsyncDefault
from bdnb_api.types.donnees.referentiel_administratif import ReferentielAdministratifRegionAPIExpert

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRegion:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: BdnbAPI) -> None:
        region = client.donnees.referentiel_administratif.region.list()
        assert_matches_type(SyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: BdnbAPI) -> None:
        region = client.donnees.referentiel_administratif.region.list(
            code_region_insee="code_region_insee",
            geom_region="geom_region",
            libelle_region="libelle_region",
            limit="limit",
            offset="offset",
            order="order",
            select="select",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(SyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: BdnbAPI) -> None:
        response = client.donnees.referentiel_administratif.region.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        region = response.parse()
        assert_matches_type(SyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: BdnbAPI) -> None:
        with client.donnees.referentiel_administratif.region.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            region = response.parse()
            assert_matches_type(SyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRegion:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncBdnbAPI) -> None:
        region = await async_client.donnees.referentiel_administratif.region.list()
        assert_matches_type(AsyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBdnbAPI) -> None:
        region = await async_client.donnees.referentiel_administratif.region.list(
            code_region_insee="code_region_insee",
            geom_region="geom_region",
            libelle_region="libelle_region",
            limit="limit",
            offset="offset",
            order="order",
            select="select",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(AsyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBdnbAPI) -> None:
        response = await async_client.donnees.referentiel_administratif.region.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        region = await response.parse()
        assert_matches_type(AsyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBdnbAPI) -> None:
        async with async_client.donnees.referentiel_administratif.region.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            region = await response.parse()
            assert_matches_type(AsyncDefault[ReferentielAdministratifRegionAPIExpert], region, path=["response"])

        assert cast(Any, response.is_closed) is True
