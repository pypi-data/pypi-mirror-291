# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bdnb_api import BdnbAPI, AsyncBdnbAPI
from tests.utils import assert_matches_type
from bdnb_api.pagination import SyncDefault, AsyncDefault
from bdnb_api.types.donnees import AdresseAPIExpert

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAdresse:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: BdnbAPI) -> None:
        adresse = client.donnees.adresse.list()
        assert_matches_type(SyncDefault[AdresseAPIExpert], adresse, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: BdnbAPI) -> None:
        adresse = client.donnees.adresse.list(
            cle_interop_adr="cle_interop_adr",
            code_commune_insee="code_commune_insee",
            code_departement_insee="code_departement_insee",
            code_postal="code_postal",
            geom_adresse="geom_adresse",
            libelle_adresse="libelle_adresse",
            libelle_commune="libelle_commune",
            limit="limit",
            nom_voie="nom_voie",
            numero="numero",
            offset="offset",
            order="order",
            rep="rep",
            select="select",
            source="source",
            type_voie="type_voie",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(SyncDefault[AdresseAPIExpert], adresse, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: BdnbAPI) -> None:
        response = client.donnees.adresse.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adresse = response.parse()
        assert_matches_type(SyncDefault[AdresseAPIExpert], adresse, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: BdnbAPI) -> None:
        with client.donnees.adresse.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adresse = response.parse()
            assert_matches_type(SyncDefault[AdresseAPIExpert], adresse, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAdresse:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncBdnbAPI) -> None:
        adresse = await async_client.donnees.adresse.list()
        assert_matches_type(AsyncDefault[AdresseAPIExpert], adresse, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBdnbAPI) -> None:
        adresse = await async_client.donnees.adresse.list(
            cle_interop_adr="cle_interop_adr",
            code_commune_insee="code_commune_insee",
            code_departement_insee="code_departement_insee",
            code_postal="code_postal",
            geom_adresse="geom_adresse",
            libelle_adresse="libelle_adresse",
            libelle_commune="libelle_commune",
            limit="limit",
            nom_voie="nom_voie",
            numero="numero",
            offset="offset",
            order="order",
            rep="rep",
            select="select",
            source="source",
            type_voie="type_voie",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(AsyncDefault[AdresseAPIExpert], adresse, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBdnbAPI) -> None:
        response = await async_client.donnees.adresse.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        adresse = await response.parse()
        assert_matches_type(AsyncDefault[AdresseAPIExpert], adresse, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBdnbAPI) -> None:
        async with async_client.donnees.adresse.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            adresse = await response.parse()
            assert_matches_type(AsyncDefault[AdresseAPIExpert], adresse, path=["response"])

        assert cast(Any, response.is_closed) is True
