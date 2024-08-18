# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bdnb_api import BdnbAPI, AsyncBdnbAPI
from tests.utils import assert_matches_type
from bdnb_api.pagination import SyncDefault, AsyncDefault
from bdnb_api.types.donnees import BatimentGroupeBdtopoBatAPIExpert

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatimentGroupeBdtopoBat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: BdnbAPI) -> None:
        batiment_groupe_bdtopo_bat = client.donnees.batiment_groupe_bdtopo_bat.list()
        assert_matches_type(
            SyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
        )

    @parametrize
    def test_method_list_with_all_params(self, client: BdnbAPI) -> None:
        batiment_groupe_bdtopo_bat = client.donnees.batiment_groupe_bdtopo_bat.list(
            altitude_sol_mean="altitude_sol_mean",
            batiment_groupe_id="batiment_groupe_id",
            code_departement_insee="code_departement_insee",
            hauteur_mean="hauteur_mean",
            l_etat="l_etat",
            l_nature="l_nature",
            l_usage_1="l_usage_1",
            l_usage_2="l_usage_2",
            limit="limit",
            max_hauteur="max_hauteur",
            offset="offset",
            order="order",
            select="select",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(
            SyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
        )

    @parametrize
    def test_raw_response_list(self, client: BdnbAPI) -> None:
        response = client.donnees.batiment_groupe_bdtopo_bat.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batiment_groupe_bdtopo_bat = response.parse()
        assert_matches_type(
            SyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
        )

    @parametrize
    def test_streaming_response_list(self, client: BdnbAPI) -> None:
        with client.donnees.batiment_groupe_bdtopo_bat.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batiment_groupe_bdtopo_bat = response.parse()
            assert_matches_type(
                SyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
            )

        assert cast(Any, response.is_closed) is True


class TestAsyncBatimentGroupeBdtopoBat:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncBdnbAPI) -> None:
        batiment_groupe_bdtopo_bat = await async_client.donnees.batiment_groupe_bdtopo_bat.list()
        assert_matches_type(
            AsyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
        )

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBdnbAPI) -> None:
        batiment_groupe_bdtopo_bat = await async_client.donnees.batiment_groupe_bdtopo_bat.list(
            altitude_sol_mean="altitude_sol_mean",
            batiment_groupe_id="batiment_groupe_id",
            code_departement_insee="code_departement_insee",
            hauteur_mean="hauteur_mean",
            l_etat="l_etat",
            l_nature="l_nature",
            l_usage_1="l_usage_1",
            l_usage_2="l_usage_2",
            limit="limit",
            max_hauteur="max_hauteur",
            offset="offset",
            order="order",
            select="select",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(
            AsyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
        )

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBdnbAPI) -> None:
        response = await async_client.donnees.batiment_groupe_bdtopo_bat.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batiment_groupe_bdtopo_bat = await response.parse()
        assert_matches_type(
            AsyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
        )

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBdnbAPI) -> None:
        async with async_client.donnees.batiment_groupe_bdtopo_bat.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batiment_groupe_bdtopo_bat = await response.parse()
            assert_matches_type(
                AsyncDefault[BatimentGroupeBdtopoBatAPIExpert], batiment_groupe_bdtopo_bat, path=["response"]
            )

        assert cast(Any, response.is_closed) is True
