# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bdnb_api import BdnbAPI, AsyncBdnbAPI
from tests.utils import assert_matches_type
from bdnb_api.pagination import SyncDefault, AsyncDefault
from bdnb_api.types.donnees import ProprietaireAPIExpert

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProprietaire:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: BdnbAPI) -> None:
        proprietaire = client.donnees.proprietaire.list()
        assert_matches_type(SyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: BdnbAPI) -> None:
        proprietaire = client.donnees.proprietaire.list(
            code_departement_insee="code_departement_insee",
            code_postal="code_postal",
            dans_majic_pm="dans_majic_pm",
            denomination="denomination",
            forme_juridique="forme_juridique",
            libelle_commune="libelle_commune",
            limit="limit",
            nb_locaux_open="nb_locaux_open",
            offset="offset",
            order="order",
            personne_id="personne_id",
            select="select",
            siren="siren",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(SyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: BdnbAPI) -> None:
        response = client.donnees.proprietaire.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        proprietaire = response.parse()
        assert_matches_type(SyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: BdnbAPI) -> None:
        with client.donnees.proprietaire.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            proprietaire = response.parse()
            assert_matches_type(SyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncProprietaire:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncBdnbAPI) -> None:
        proprietaire = await async_client.donnees.proprietaire.list()
        assert_matches_type(AsyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBdnbAPI) -> None:
        proprietaire = await async_client.donnees.proprietaire.list(
            code_departement_insee="code_departement_insee",
            code_postal="code_postal",
            dans_majic_pm="dans_majic_pm",
            denomination="denomination",
            forme_juridique="forme_juridique",
            libelle_commune="libelle_commune",
            limit="limit",
            nb_locaux_open="nb_locaux_open",
            offset="offset",
            order="order",
            personne_id="personne_id",
            select="select",
            siren="siren",
            range="Range",
            range_unit="Range-Unit",
        )
        assert_matches_type(AsyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBdnbAPI) -> None:
        response = await async_client.donnees.proprietaire.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        proprietaire = await response.parse()
        assert_matches_type(AsyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBdnbAPI) -> None:
        async with async_client.donnees.proprietaire.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            proprietaire = await response.parse()
            assert_matches_type(AsyncDefault[ProprietaireAPIExpert], proprietaire, path=["response"])

        assert cast(Any, response.is_closed) is True
