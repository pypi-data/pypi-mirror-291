# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date

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
from ...types.donnees import rel_batiment_groupe_siret_complet_list_params
from ...types.rel_batiment_groupe_siret_complet_api_expert import RelBatimentGroupeSiretCompletAPIExpert

__all__ = ["RelBatimentGroupeSiretCompletResource", "AsyncRelBatimentGroupeSiretCompletResource"]


class RelBatimentGroupeSiretCompletResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RelBatimentGroupeSiretCompletResourceWithRawResponse:
        return RelBatimentGroupeSiretCompletResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RelBatimentGroupeSiretCompletResourceWithStreamingResponse:
        return RelBatimentGroupeSiretCompletResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        activite_registre_metier: str | NotGiven = NOT_GIVEN,
        batiment_groupe_id: str | NotGiven = NOT_GIVEN,
        cle_interop_adr: str | NotGiven = NOT_GIVEN,
        code_activite_principale: str | NotGiven = NOT_GIVEN,
        code_departement_insee: str | NotGiven = NOT_GIVEN,
        date_creation: Union[str, date] | NotGiven = NOT_GIVEN,
        date_dernier_traitement: Union[str, date] | NotGiven = NOT_GIVEN,
        denomination_etablissement: str | NotGiven = NOT_GIVEN,
        etat_administratif_actif: str | NotGiven = NOT_GIVEN,
        libelle_activite_principale: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        nic: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        order: str | NotGiven = NOT_GIVEN,
        select: str | NotGiven = NOT_GIVEN,
        siege_social: str | NotGiven = NOT_GIVEN,
        siren: str | NotGiven = NOT_GIVEN,
        siret: str | NotGiven = NOT_GIVEN,
        range: str | NotGiven = NOT_GIVEN,
        range_unit: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDefault[RelBatimentGroupeSiretCompletAPIExpert]:
        """
        Table de relation entre les bâtiments de la BDNB et les SIRET.

        Args:
          activite_registre_metier: Activité principale de l'établissement au Registre des Métiers. Cette variable,
              complémentaire à l'activité principale de l'établissement, ne concerne que les
              établissements relevant de l'artisanat (artisans, artisans-commerà§ants et
              sociétés artisanales). Elle caractérise l'activité selon la Nomenclature
              d'Activités Franà§aise de l'Artisanat (NAFA). La variable n'est pas disponible
              au niveau unité légale.

          batiment_groupe_id: Identifiant du groupe de bâtiment au sens de la BDNB

          cle_interop_adr: Clé d'interopérabilité de l'adresse postale

          code_activite_principale: Code de l'activité principale de l'établissement, lors de son inscription au
              répertoire APET. Il permet l'identification de la branche d'activité principale
              pour chaque établissement.

          code_departement_insee: Code département INSEE

          date_creation: La date de création de l'unité légale - correspond à la date qui figure dans la
              déclaration déposée au Centres de Formalités des Entreprises (CFE) compétent.

          date_dernier_traitement: Date du dernier traitement de l'unité légale dans le répertoire Sirene.

          denomination_etablissement: Cette variable désigne le nom sous lequel l'établissement est connu du grand
              public (nom commercial de l'établissement).

          etat_administratif_actif: à‰tat administratif de l'établissement. Si l'établissement est signalé comme
              actif alors la variable est indiquée comme 'Vrai'.

          libelle_activite_principale: Libellé de l'activité principale de l'établissement, lors de son inscription au
              répertoire APET.

          limit: Limiting and Pagination

          nic: Numéro interne de classement (Nic) de l'établissement siège de l'établissement.

          offset: Limiting and Pagination

          order: Ordering

          select: Filtering Columns

          siege_social: Indique si l'établissement est le siège social

          siren: Siret de l'établissement.

          siret: Siret de l'établissement.

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
            "/donnees/rel_batiment_groupe_siret_complet",
            page=SyncDefault[RelBatimentGroupeSiretCompletAPIExpert],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "activite_registre_metier": activite_registre_metier,
                        "batiment_groupe_id": batiment_groupe_id,
                        "cle_interop_adr": cle_interop_adr,
                        "code_activite_principale": code_activite_principale,
                        "code_departement_insee": code_departement_insee,
                        "date_creation": date_creation,
                        "date_dernier_traitement": date_dernier_traitement,
                        "denomination_etablissement": denomination_etablissement,
                        "etat_administratif_actif": etat_administratif_actif,
                        "libelle_activite_principale": libelle_activite_principale,
                        "limit": limit,
                        "nic": nic,
                        "offset": offset,
                        "order": order,
                        "select": select,
                        "siege_social": siege_social,
                        "siren": siren,
                        "siret": siret,
                    },
                    rel_batiment_groupe_siret_complet_list_params.RelBatimentGroupeSiretCompletListParams,
                ),
            ),
            model=RelBatimentGroupeSiretCompletAPIExpert,
        )


class AsyncRelBatimentGroupeSiretCompletResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRelBatimentGroupeSiretCompletResourceWithRawResponse:
        return AsyncRelBatimentGroupeSiretCompletResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRelBatimentGroupeSiretCompletResourceWithStreamingResponse:
        return AsyncRelBatimentGroupeSiretCompletResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        activite_registre_metier: str | NotGiven = NOT_GIVEN,
        batiment_groupe_id: str | NotGiven = NOT_GIVEN,
        cle_interop_adr: str | NotGiven = NOT_GIVEN,
        code_activite_principale: str | NotGiven = NOT_GIVEN,
        code_departement_insee: str | NotGiven = NOT_GIVEN,
        date_creation: Union[str, date] | NotGiven = NOT_GIVEN,
        date_dernier_traitement: Union[str, date] | NotGiven = NOT_GIVEN,
        denomination_etablissement: str | NotGiven = NOT_GIVEN,
        etat_administratif_actif: str | NotGiven = NOT_GIVEN,
        libelle_activite_principale: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        nic: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        order: str | NotGiven = NOT_GIVEN,
        select: str | NotGiven = NOT_GIVEN,
        siege_social: str | NotGiven = NOT_GIVEN,
        siren: str | NotGiven = NOT_GIVEN,
        siret: str | NotGiven = NOT_GIVEN,
        range: str | NotGiven = NOT_GIVEN,
        range_unit: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[RelBatimentGroupeSiretCompletAPIExpert, AsyncDefault[RelBatimentGroupeSiretCompletAPIExpert]]:
        """
        Table de relation entre les bâtiments de la BDNB et les SIRET.

        Args:
          activite_registre_metier: Activité principale de l'établissement au Registre des Métiers. Cette variable,
              complémentaire à l'activité principale de l'établissement, ne concerne que les
              établissements relevant de l'artisanat (artisans, artisans-commerà§ants et
              sociétés artisanales). Elle caractérise l'activité selon la Nomenclature
              d'Activités Franà§aise de l'Artisanat (NAFA). La variable n'est pas disponible
              au niveau unité légale.

          batiment_groupe_id: Identifiant du groupe de bâtiment au sens de la BDNB

          cle_interop_adr: Clé d'interopérabilité de l'adresse postale

          code_activite_principale: Code de l'activité principale de l'établissement, lors de son inscription au
              répertoire APET. Il permet l'identification de la branche d'activité principale
              pour chaque établissement.

          code_departement_insee: Code département INSEE

          date_creation: La date de création de l'unité légale - correspond à la date qui figure dans la
              déclaration déposée au Centres de Formalités des Entreprises (CFE) compétent.

          date_dernier_traitement: Date du dernier traitement de l'unité légale dans le répertoire Sirene.

          denomination_etablissement: Cette variable désigne le nom sous lequel l'établissement est connu du grand
              public (nom commercial de l'établissement).

          etat_administratif_actif: à‰tat administratif de l'établissement. Si l'établissement est signalé comme
              actif alors la variable est indiquée comme 'Vrai'.

          libelle_activite_principale: Libellé de l'activité principale de l'établissement, lors de son inscription au
              répertoire APET.

          limit: Limiting and Pagination

          nic: Numéro interne de classement (Nic) de l'établissement siège de l'établissement.

          offset: Limiting and Pagination

          order: Ordering

          select: Filtering Columns

          siege_social: Indique si l'établissement est le siège social

          siren: Siret de l'établissement.

          siret: Siret de l'établissement.

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
            "/donnees/rel_batiment_groupe_siret_complet",
            page=AsyncDefault[RelBatimentGroupeSiretCompletAPIExpert],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "activite_registre_metier": activite_registre_metier,
                        "batiment_groupe_id": batiment_groupe_id,
                        "cle_interop_adr": cle_interop_adr,
                        "code_activite_principale": code_activite_principale,
                        "code_departement_insee": code_departement_insee,
                        "date_creation": date_creation,
                        "date_dernier_traitement": date_dernier_traitement,
                        "denomination_etablissement": denomination_etablissement,
                        "etat_administratif_actif": etat_administratif_actif,
                        "libelle_activite_principale": libelle_activite_principale,
                        "limit": limit,
                        "nic": nic,
                        "offset": offset,
                        "order": order,
                        "select": select,
                        "siege_social": siege_social,
                        "siren": siren,
                        "siret": siret,
                    },
                    rel_batiment_groupe_siret_complet_list_params.RelBatimentGroupeSiretCompletListParams,
                ),
            ),
            model=RelBatimentGroupeSiretCompletAPIExpert,
        )


class RelBatimentGroupeSiretCompletResourceWithRawResponse:
    def __init__(self, rel_batiment_groupe_siret_complet: RelBatimentGroupeSiretCompletResource) -> None:
        self._rel_batiment_groupe_siret_complet = rel_batiment_groupe_siret_complet

        self.list = to_raw_response_wrapper(
            rel_batiment_groupe_siret_complet.list,
        )


class AsyncRelBatimentGroupeSiretCompletResourceWithRawResponse:
    def __init__(self, rel_batiment_groupe_siret_complet: AsyncRelBatimentGroupeSiretCompletResource) -> None:
        self._rel_batiment_groupe_siret_complet = rel_batiment_groupe_siret_complet

        self.list = async_to_raw_response_wrapper(
            rel_batiment_groupe_siret_complet.list,
        )


class RelBatimentGroupeSiretCompletResourceWithStreamingResponse:
    def __init__(self, rel_batiment_groupe_siret_complet: RelBatimentGroupeSiretCompletResource) -> None:
        self._rel_batiment_groupe_siret_complet = rel_batiment_groupe_siret_complet

        self.list = to_streamed_response_wrapper(
            rel_batiment_groupe_siret_complet.list,
        )


class AsyncRelBatimentGroupeSiretCompletResourceWithStreamingResponse:
    def __init__(self, rel_batiment_groupe_siret_complet: AsyncRelBatimentGroupeSiretCompletResource) -> None:
        self._rel_batiment_groupe_siret_complet = rel_batiment_groupe_siret_complet

        self.list = async_to_streamed_response_wrapper(
            rel_batiment_groupe_siret_complet.list,
        )
