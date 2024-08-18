# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncDefault, AsyncDefault
from ..._base_client import AsyncPaginator, make_request_options
from ...types.donnees import rel_batiment_groupe_proprietaire_siren_open_list_params
from ...types.donnees.rel_batiment_groupe_proprietaire_siren_openapi_expert import (
    RelBatimentGroupeProprietaireSirenOpenAPIExpert,
)

__all__ = ["RelBatimentGroupeProprietaireSirenOpenResource", "AsyncRelBatimentGroupeProprietaireSirenOpenResource"]


class RelBatimentGroupeProprietaireSirenOpenResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RelBatimentGroupeProprietaireSirenOpenResourceWithRawResponse:
        return RelBatimentGroupeProprietaireSirenOpenResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RelBatimentGroupeProprietaireSirenOpenResourceWithStreamingResponse:
        return RelBatimentGroupeProprietaireSirenOpenResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        bat_prop_denomination_proprietaire: str | NotGiven = NOT_GIVEN,
        batiment_groupe_id: str | NotGiven = NOT_GIVEN,
        code_departement_insee: str | NotGiven = NOT_GIVEN,
        dans_majic_pm: str | NotGiven = NOT_GIVEN,
        is_bailleur: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        nb_locaux_open: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        order: str | NotGiven = NOT_GIVEN,
        select: str | NotGiven = NOT_GIVEN,
        siren: str | NotGiven = NOT_GIVEN,
        range: str | NotGiven = NOT_GIVEN,
        range_unit: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDefault[RelBatimentGroupeProprietaireSirenOpenAPIExpert]:
        """
        Table de relation entre les proprietaires et les groupes de bâtiment (la version
        open filtre sur la colonne `dans_majic_pm)

        Args:
          bat_prop_denomination_proprietaire: TODO

          batiment_groupe_id: Identifiant du groupe de bâtiment au sens de la BDNB

          code_departement_insee: Code département INSEE

          dans_majic_pm: (majic_pm) Ce propriétaire possède des bâtiments déclarés dans majic_pm

          is_bailleur: Vrai si le propriétaire est un bailleur social

          limit: Limiting and Pagination

          nb_locaux_open: (majic_pm) nombre de locaux déclarés dans majic_pm

          offset: Limiting and Pagination

          order: Ordering

          select: Filtering Columns

          siren: Numéro de SIREN de la personne morale (FF)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "Range": range,
                    "Range-Unit": range_unit,
                }
            ),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            "/donnees/rel_batiment_groupe_proprietaire_siren_open",
            page=SyncDefault[RelBatimentGroupeProprietaireSirenOpenAPIExpert],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "bat_prop_denomination_proprietaire": bat_prop_denomination_proprietaire,
                        "batiment_groupe_id": batiment_groupe_id,
                        "code_departement_insee": code_departement_insee,
                        "dans_majic_pm": dans_majic_pm,
                        "is_bailleur": is_bailleur,
                        "limit": limit,
                        "nb_locaux_open": nb_locaux_open,
                        "offset": offset,
                        "order": order,
                        "select": select,
                        "siren": siren,
                    },
                    rel_batiment_groupe_proprietaire_siren_open_list_params.RelBatimentGroupeProprietaireSirenOpenListParams,
                ),
            ),
            model=RelBatimentGroupeProprietaireSirenOpenAPIExpert,
        )


class AsyncRelBatimentGroupeProprietaireSirenOpenResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRelBatimentGroupeProprietaireSirenOpenResourceWithRawResponse:
        return AsyncRelBatimentGroupeProprietaireSirenOpenResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRelBatimentGroupeProprietaireSirenOpenResourceWithStreamingResponse:
        return AsyncRelBatimentGroupeProprietaireSirenOpenResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        bat_prop_denomination_proprietaire: str | NotGiven = NOT_GIVEN,
        batiment_groupe_id: str | NotGiven = NOT_GIVEN,
        code_departement_insee: str | NotGiven = NOT_GIVEN,
        dans_majic_pm: str | NotGiven = NOT_GIVEN,
        is_bailleur: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        nb_locaux_open: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        order: str | NotGiven = NOT_GIVEN,
        select: str | NotGiven = NOT_GIVEN,
        siren: str | NotGiven = NOT_GIVEN,
        range: str | NotGiven = NOT_GIVEN,
        range_unit: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[
        RelBatimentGroupeProprietaireSirenOpenAPIExpert, AsyncDefault[RelBatimentGroupeProprietaireSirenOpenAPIExpert]
    ]:
        """
        Table de relation entre les proprietaires et les groupes de bâtiment (la version
        open filtre sur la colonne `dans_majic_pm)

        Args:
          bat_prop_denomination_proprietaire: TODO

          batiment_groupe_id: Identifiant du groupe de bâtiment au sens de la BDNB

          code_departement_insee: Code département INSEE

          dans_majic_pm: (majic_pm) Ce propriétaire possède des bâtiments déclarés dans majic_pm

          is_bailleur: Vrai si le propriétaire est un bailleur social

          limit: Limiting and Pagination

          nb_locaux_open: (majic_pm) nombre de locaux déclarés dans majic_pm

          offset: Limiting and Pagination

          order: Ordering

          select: Filtering Columns

          siren: Numéro de SIREN de la personne morale (FF)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "Range": range,
                    "Range-Unit": range_unit,
                }
            ),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            "/donnees/rel_batiment_groupe_proprietaire_siren_open",
            page=AsyncDefault[RelBatimentGroupeProprietaireSirenOpenAPIExpert],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "bat_prop_denomination_proprietaire": bat_prop_denomination_proprietaire,
                        "batiment_groupe_id": batiment_groupe_id,
                        "code_departement_insee": code_departement_insee,
                        "dans_majic_pm": dans_majic_pm,
                        "is_bailleur": is_bailleur,
                        "limit": limit,
                        "nb_locaux_open": nb_locaux_open,
                        "offset": offset,
                        "order": order,
                        "select": select,
                        "siren": siren,
                    },
                    rel_batiment_groupe_proprietaire_siren_open_list_params.RelBatimentGroupeProprietaireSirenOpenListParams,
                ),
            ),
            model=RelBatimentGroupeProprietaireSirenOpenAPIExpert,
        )


class RelBatimentGroupeProprietaireSirenOpenResourceWithRawResponse:
    def __init__(
        self, rel_batiment_groupe_proprietaire_siren_open: RelBatimentGroupeProprietaireSirenOpenResource
    ) -> None:
        self._rel_batiment_groupe_proprietaire_siren_open = rel_batiment_groupe_proprietaire_siren_open

        self.list = to_raw_response_wrapper(
            rel_batiment_groupe_proprietaire_siren_open.list,
        )


class AsyncRelBatimentGroupeProprietaireSirenOpenResourceWithRawResponse:
    def __init__(
        self, rel_batiment_groupe_proprietaire_siren_open: AsyncRelBatimentGroupeProprietaireSirenOpenResource
    ) -> None:
        self._rel_batiment_groupe_proprietaire_siren_open = rel_batiment_groupe_proprietaire_siren_open

        self.list = async_to_raw_response_wrapper(
            rel_batiment_groupe_proprietaire_siren_open.list,
        )


class RelBatimentGroupeProprietaireSirenOpenResourceWithStreamingResponse:
    def __init__(
        self, rel_batiment_groupe_proprietaire_siren_open: RelBatimentGroupeProprietaireSirenOpenResource
    ) -> None:
        self._rel_batiment_groupe_proprietaire_siren_open = rel_batiment_groupe_proprietaire_siren_open

        self.list = to_streamed_response_wrapper(
            rel_batiment_groupe_proprietaire_siren_open.list,
        )


class AsyncRelBatimentGroupeProprietaireSirenOpenResourceWithStreamingResponse:
    def __init__(
        self, rel_batiment_groupe_proprietaire_siren_open: AsyncRelBatimentGroupeProprietaireSirenOpenResource
    ) -> None:
        self._rel_batiment_groupe_proprietaire_siren_open = rel_batiment_groupe_proprietaire_siren_open

        self.list = async_to_streamed_response_wrapper(
            rel_batiment_groupe_proprietaire_siren_open.list,
        )
