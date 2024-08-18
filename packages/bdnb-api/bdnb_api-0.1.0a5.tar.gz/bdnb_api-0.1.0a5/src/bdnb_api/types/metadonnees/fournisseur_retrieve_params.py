# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["FournisseurRetrieveParams"]


class FournisseurRetrieveParams(TypedDict, total=False):
    acronyme: str
    """Acronyme du fournisseur de données"""

    denomination_fournisseur: str
    """Dénomination du fournisseur de données"""

    description: str
    """Description du fournisseur de données"""

    limit: str
    """Limiting and Pagination"""

    offset: str
    """Limiting and Pagination"""

    order: str
    """Ordering"""

    select: str
    """Filtering Columns"""

    range: Annotated[str, PropertyInfo(alias="Range")]

    range_unit: Annotated[str, PropertyInfo(alias="Range-Unit")]
