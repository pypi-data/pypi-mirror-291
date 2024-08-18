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
from ...types.donnees import batiment_groupe_indicateur_reseau_chaud_froid_list_params
from ...types.donnees.batiment_groupe_indicateur_reseau_chaud_froid_api_expert import (
    BatimentGroupeIndicateurReseauChaudFroidAPIExpert,
)

__all__ = ["BatimentGroupeIndicateurReseauChaudFroidResource", "AsyncBatimentGroupeIndicateurReseauChaudFroidResource"]


class BatimentGroupeIndicateurReseauChaudFroidResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatimentGroupeIndicateurReseauChaudFroidResourceWithRawResponse:
        return BatimentGroupeIndicateurReseauChaudFroidResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatimentGroupeIndicateurReseauChaudFroidResourceWithStreamingResponse:
        return BatimentGroupeIndicateurReseauChaudFroidResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        batiment_groupe_id: str | NotGiven = NOT_GIVEN,
        code_departement_insee: str | NotGiven = NOT_GIVEN,
        consommation_chaleur_par_rapport_distance_au_reseau: str | NotGiven = NOT_GIVEN,
        id_reseau: str | NotGiven = NOT_GIVEN,
        id_reseau_bdnb: str | NotGiven = NOT_GIVEN,
        indicateur_distance_au_reseau: str | NotGiven = NOT_GIVEN,
        indicateur_systeme_chauffage: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        order: str | NotGiven = NOT_GIVEN,
        potentiel_obligation_raccordement: str | NotGiven = NOT_GIVEN,
        potentiel_raccordement_reseau_chaleur: str | NotGiven = NOT_GIVEN,
        select: str | NotGiven = NOT_GIVEN,
        range: str | NotGiven = NOT_GIVEN,
        range_unit: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDefault[BatimentGroupeIndicateurReseauChaudFroidAPIExpert]:
        """
        Indicateur de raccordement et de potentiel de raccordement aux réseaux de
        chaleur et de froid urbains construit à l'aide des données de 'France Chaleur
        Urbaine' et les 'Données Locales de l'Energie'.

        Args:
          batiment_groupe_id: (bdnb) Clé d'Intéropérabilité du bâtiment dans la BDNB

          code_departement_insee: Code département INSEE

          consommation_chaleur_par_rapport_distance_au_reseau: Indication sur la consommation de chaleur du bâtiment et sa distance au réseau.
              Plus un bâtiment consomme plus celui-ci peut àªtre éloigné du réseau et malgré
              tout àªtre raccordé. Ici, si la distance entre le bâtiment et le réseau est
              suffisamment proche par rapport à sa consommation, la consommation est noté
              'suffisante', sinon elle est notée 'trop faible'.

          id_reseau: (France chaleur urbaine) Identifiant national du réseau.

          id_reseau_bdnb: Identifiant BDNB, lié au réseau de chaleur, car des données sources ne disposent
              pas d'identifiant unique pour chacune des entrées (traces et points).

          indicateur_distance_au_reseau: Indication sur la distance entre le bâtiment et le point au réseau de chaleur le
              plus proche en vue d'un potentiel raccordement au réseau.

          limit: Limiting and Pagination

          offset: Limiting and Pagination

          order: Ordering

          potentiel_obligation_raccordement: Indique si le bâtiment est éventuellement dans l'obligation de se raccorder lors
              de certains travaux de rénovation. Pour que potentiel_obligation_raccordement
              soit possible, le bâtiment doit àªtre situé à moins de 100m d'un réseau classé
              et son système de chauffage indiqué comme collectif. Attention, cet indicateur
              n'est qu'à titre d'information.

          potentiel_raccordement_reseau_chaleur: Indicateur de potentiel de raccordement au réseau de chaleur. L'indicateur
              dépend de la distance entre le bâtiment et le réseau et du type de circuit de
              chauffage existant du bâtiment. Enfin, si le bâtiment est déjà raccordé alors il
              est indiqué comme tel.

          select: Filtering Columns

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
            "/donnees/batiment_groupe_indicateur_reseau_chaud_froid",
            page=SyncDefault[BatimentGroupeIndicateurReseauChaudFroidAPIExpert],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "batiment_groupe_id": batiment_groupe_id,
                        "code_departement_insee": code_departement_insee,
                        "consommation_chaleur_par_rapport_distance_au_reseau": consommation_chaleur_par_rapport_distance_au_reseau,
                        "id_reseau": id_reseau,
                        "id_reseau_bdnb": id_reseau_bdnb,
                        "indicateur_distance_au_reseau": indicateur_distance_au_reseau,
                        "indicateur_systeme_chauffage": indicateur_systeme_chauffage,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "potentiel_obligation_raccordement": potentiel_obligation_raccordement,
                        "potentiel_raccordement_reseau_chaleur": potentiel_raccordement_reseau_chaleur,
                        "select": select,
                    },
                    batiment_groupe_indicateur_reseau_chaud_froid_list_params.BatimentGroupeIndicateurReseauChaudFroidListParams,
                ),
            ),
            model=BatimentGroupeIndicateurReseauChaudFroidAPIExpert,
        )


class AsyncBatimentGroupeIndicateurReseauChaudFroidResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatimentGroupeIndicateurReseauChaudFroidResourceWithRawResponse:
        return AsyncBatimentGroupeIndicateurReseauChaudFroidResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatimentGroupeIndicateurReseauChaudFroidResourceWithStreamingResponse:
        return AsyncBatimentGroupeIndicateurReseauChaudFroidResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        batiment_groupe_id: str | NotGiven = NOT_GIVEN,
        code_departement_insee: str | NotGiven = NOT_GIVEN,
        consommation_chaleur_par_rapport_distance_au_reseau: str | NotGiven = NOT_GIVEN,
        id_reseau: str | NotGiven = NOT_GIVEN,
        id_reseau_bdnb: str | NotGiven = NOT_GIVEN,
        indicateur_distance_au_reseau: str | NotGiven = NOT_GIVEN,
        indicateur_systeme_chauffage: str | NotGiven = NOT_GIVEN,
        limit: str | NotGiven = NOT_GIVEN,
        offset: str | NotGiven = NOT_GIVEN,
        order: str | NotGiven = NOT_GIVEN,
        potentiel_obligation_raccordement: str | NotGiven = NOT_GIVEN,
        potentiel_raccordement_reseau_chaleur: str | NotGiven = NOT_GIVEN,
        select: str | NotGiven = NOT_GIVEN,
        range: str | NotGiven = NOT_GIVEN,
        range_unit: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[
        BatimentGroupeIndicateurReseauChaudFroidAPIExpert,
        AsyncDefault[BatimentGroupeIndicateurReseauChaudFroidAPIExpert],
    ]:
        """
        Indicateur de raccordement et de potentiel de raccordement aux réseaux de
        chaleur et de froid urbains construit à l'aide des données de 'France Chaleur
        Urbaine' et les 'Données Locales de l'Energie'.

        Args:
          batiment_groupe_id: (bdnb) Clé d'Intéropérabilité du bâtiment dans la BDNB

          code_departement_insee: Code département INSEE

          consommation_chaleur_par_rapport_distance_au_reseau: Indication sur la consommation de chaleur du bâtiment et sa distance au réseau.
              Plus un bâtiment consomme plus celui-ci peut àªtre éloigné du réseau et malgré
              tout àªtre raccordé. Ici, si la distance entre le bâtiment et le réseau est
              suffisamment proche par rapport à sa consommation, la consommation est noté
              'suffisante', sinon elle est notée 'trop faible'.

          id_reseau: (France chaleur urbaine) Identifiant national du réseau.

          id_reseau_bdnb: Identifiant BDNB, lié au réseau de chaleur, car des données sources ne disposent
              pas d'identifiant unique pour chacune des entrées (traces et points).

          indicateur_distance_au_reseau: Indication sur la distance entre le bâtiment et le point au réseau de chaleur le
              plus proche en vue d'un potentiel raccordement au réseau.

          limit: Limiting and Pagination

          offset: Limiting and Pagination

          order: Ordering

          potentiel_obligation_raccordement: Indique si le bâtiment est éventuellement dans l'obligation de se raccorder lors
              de certains travaux de rénovation. Pour que potentiel_obligation_raccordement
              soit possible, le bâtiment doit àªtre situé à moins de 100m d'un réseau classé
              et son système de chauffage indiqué comme collectif. Attention, cet indicateur
              n'est qu'à titre d'information.

          potentiel_raccordement_reseau_chaleur: Indicateur de potentiel de raccordement au réseau de chaleur. L'indicateur
              dépend de la distance entre le bâtiment et le réseau et du type de circuit de
              chauffage existant du bâtiment. Enfin, si le bâtiment est déjà raccordé alors il
              est indiqué comme tel.

          select: Filtering Columns

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
            "/donnees/batiment_groupe_indicateur_reseau_chaud_froid",
            page=AsyncDefault[BatimentGroupeIndicateurReseauChaudFroidAPIExpert],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "batiment_groupe_id": batiment_groupe_id,
                        "code_departement_insee": code_departement_insee,
                        "consommation_chaleur_par_rapport_distance_au_reseau": consommation_chaleur_par_rapport_distance_au_reseau,
                        "id_reseau": id_reseau,
                        "id_reseau_bdnb": id_reseau_bdnb,
                        "indicateur_distance_au_reseau": indicateur_distance_au_reseau,
                        "indicateur_systeme_chauffage": indicateur_systeme_chauffage,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "potentiel_obligation_raccordement": potentiel_obligation_raccordement,
                        "potentiel_raccordement_reseau_chaleur": potentiel_raccordement_reseau_chaleur,
                        "select": select,
                    },
                    batiment_groupe_indicateur_reseau_chaud_froid_list_params.BatimentGroupeIndicateurReseauChaudFroidListParams,
                ),
            ),
            model=BatimentGroupeIndicateurReseauChaudFroidAPIExpert,
        )


class BatimentGroupeIndicateurReseauChaudFroidResourceWithRawResponse:
    def __init__(
        self, batiment_groupe_indicateur_reseau_chaud_froid: BatimentGroupeIndicateurReseauChaudFroidResource
    ) -> None:
        self._batiment_groupe_indicateur_reseau_chaud_froid = batiment_groupe_indicateur_reseau_chaud_froid

        self.list = to_raw_response_wrapper(
            batiment_groupe_indicateur_reseau_chaud_froid.list,
        )


class AsyncBatimentGroupeIndicateurReseauChaudFroidResourceWithRawResponse:
    def __init__(
        self, batiment_groupe_indicateur_reseau_chaud_froid: AsyncBatimentGroupeIndicateurReseauChaudFroidResource
    ) -> None:
        self._batiment_groupe_indicateur_reseau_chaud_froid = batiment_groupe_indicateur_reseau_chaud_froid

        self.list = async_to_raw_response_wrapper(
            batiment_groupe_indicateur_reseau_chaud_froid.list,
        )


class BatimentGroupeIndicateurReseauChaudFroidResourceWithStreamingResponse:
    def __init__(
        self, batiment_groupe_indicateur_reseau_chaud_froid: BatimentGroupeIndicateurReseauChaudFroidResource
    ) -> None:
        self._batiment_groupe_indicateur_reseau_chaud_froid = batiment_groupe_indicateur_reseau_chaud_froid

        self.list = to_streamed_response_wrapper(
            batiment_groupe_indicateur_reseau_chaud_froid.list,
        )


class AsyncBatimentGroupeIndicateurReseauChaudFroidResourceWithStreamingResponse:
    def __init__(
        self, batiment_groupe_indicateur_reseau_chaud_froid: AsyncBatimentGroupeIndicateurReseauChaudFroidResource
    ) -> None:
        self._batiment_groupe_indicateur_reseau_chaud_froid = batiment_groupe_indicateur_reseau_chaud_froid

        self.list = async_to_streamed_response_wrapper(
            batiment_groupe_indicateur_reseau_chaud_froid.list,
        )
