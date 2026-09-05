"""Deterministic summary for a geographic risk assessment."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class PromoteurReport:
    faisabilite_construction: str
    impact_valeur_fonciere: str
    perspective_assurabilite: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generer_rapport_promoteur(
    score_moyen: float,
    rating_global: str,
    perils: dict[str, Any],
    land_only: bool,
    worst_case_peril: str | None,
    worst_case_score: float,
    nb_points_valides: int,
    nb_points_erreur: int,
) -> PromoteurReport:
    """Build a conservative, deterministic report from zone statistics."""
    notes: list[str] = []
    high_critical = any(
        float(getattr(peril, "pct_critique", 0.0)) >= 30.0
        for peril in perils.values()
    )

    if score_moyen < 40 and worst_case_score < 60:
        faisabilite = "Bonne faisabilité de construction dans la zone."
        valeur = "Impact sur la valeur foncière faible ou négligeable."
        assurance = "Perspective d'assurabilité favorable."
    else:
        faisabilite = "Faisabilité de construction conditionnelle, sous réserve d'études et de mesures de prévention."
        valeur = "Risque de décote de la valeur foncière à examiner."
        assurance = "Assurabilité potentiellement compromise ou soumise à conditions."

    if nb_points_erreur:
        notes.append(f"{nb_points_erreur} point(s) de la zone n'ont pas pu être évalués.")
    if worst_case_peril and worst_case_score >= 70:
        notes.append(f"Point chaud identifié sur l'aléa {worst_case_peril} (worst case : {worst_case_score:.0f}/100).")
    if high_critical:
        notes.append("Une part importante des points présente un niveau critique pour au moins un aléa.")
    if land_only:
        notes.append("Terrain nu : les caractéristiques du bâtiment et les données BDNB ne sont pas disponibles.")

    return PromoteurReport(
        faisabilite_construction=faisabilite,
        impact_valeur_fonciere=valeur,
        perspective_assurabilite=assurance,
        notes=notes,
    )
