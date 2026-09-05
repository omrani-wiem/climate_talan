"""Aggregation of climate risk scores over a geographic area."""

from __future__ import annotations

import asyncio
import math
import statistics
from dataclasses import asdict, dataclass, field
from typing import Any, Awaitable, Callable

from app.scoring.risk_model import compute_risk_scores


@dataclass
class DistributionPeril:
    scores: list[float] = field(default_factory=list)
    min_score: float = 0.0
    max_score: float = 0.0
    moyenne: float = 0.0
    mediane: float = 0.0
    ecart_type: float = 0.0
    pct_faible: float = 0.0
    pct_modere: float = 0.0
    pct_eleve: float = 0.0
    pct_critique: float = 0.0
    worst_case: float = 0.0


@dataclass
class RatingZone:
    nb_points: int = 0
    nb_points_valides: int = 0
    nb_points_erreur: int = 0
    score_moyen: float = 0.0
    score_pondere: float = 0.0
    rating_global: str = "Indetermine"
    perils: dict[str, DistributionPeril] = field(default_factory=dict)
    worst_case_peril: str | None = None
    worst_case_score: float = 0.0
    message: str = ""
    land_only: bool = False


def _generer_grille_rectangulaire(
    bounds: tuple[float, float, float, float],
    spacing_km: float = 1.0,
    max_points: int = 500,
) -> list[tuple[float, float]]:
    """Generate an approximately regular grid inside (south, west, north, east)."""
    south, west, north, east = bounds
    if north < south or east < west or spacing_km <= 0 or max_points <= 0:
        return []

    lat_step = spacing_km / 111.0
    points: list[tuple[float, float]] = []
    lat = south
    while lat <= north + 1e-12 and len(points) < max_points:
        lon_step = spacing_km / max(111.0 * math.cos(math.radians(lat)), 1.0)
        lon = west
        while lon <= east + 1e-12 and len(points) < max_points:
            points.append((round(lat, 6), round(lon, 6)))
            lon += lon_step
        lat += lat_step
    return points


def _rating_from_mean(mean_score: float, worst_case: float) -> str:
    """Classify a zone while allowing a severe local worst case to dominate."""
    score = max(float(mean_score), float(worst_case))
    if score < 20:
        return "Très faible"
    if score < 40:
        return "Faible"
    if score < 60:
        return "Modéré"
    if score < 70:
        return "Élevé"
    return "Élevé"


def _distribution(scores: list[float]) -> DistributionPeril:
    if not scores:
        return DistributionPeril()
    total = len(scores)
    faible = sum(score < 40 for score in scores)
    modere = sum(40 <= score < 60 for score in scores)
    eleve = sum(60 <= score < 80 for score in scores)
    critique = sum(score >= 80 for score in scores)
    return DistributionPeril(
        scores=scores,
        min_score=min(scores),
        max_score=max(scores),
        moyenne=statistics.fmean(scores),
        mediane=statistics.median(scores),
        ecart_type=statistics.pstdev(scores) if len(scores) > 1 else 0.0,
        pct_faible=100 * faible / total,
        pct_modere=100 * modere / total,
        pct_eleve=100 * eleve / total,
        pct_critique=100 * critique / total,
        worst_case=max(scores),
    )


def rating_zone_to_dict(rating: RatingZone) -> dict[str, Any]:
    result = asdict(rating)
    result["perils"] = {name: asdict(peril) for name, peril in rating.perils.items()}
    return result


def _address_for_point(lat: float, lon: float) -> str:
    return f"{lat:.6f},{lon:.6f}"


def _minimal_building_data() -> dict[str, Any]:
    """Offline fallback used when a zone assessment has no collector."""
    return {
        "adresse": {},
        "bdnb": None,
        "georisques": {},
        "climat_open_meteo": {
            "reference_2015_2024": {},
            "projection_2041_2050": {},
        },
    }


async def run_zone_risk_assessment(
    bounds: tuple[float, float, float, float],
    spacing_km: float = 1.0,
    max_points: int = 500,
    max_concurrency: int = 8,
    land_only: bool = False,
    collector: Callable[[str], Awaitable[dict[str, Any]]] | None = None,
) -> RatingZone:
    """Collect and aggregate risk scores for points in a geographic rectangle."""
    points = _generer_grille_rectangulaire(bounds, spacing_km, max_points)
    rating = RatingZone(nb_points=len(points), land_only=land_only)
    if not points:
        rating.message = "Aucun point dans la zone"
        return rating

    semaphore = asyncio.Semaphore(max(1, max_concurrency))

    async def assess(point: tuple[float, float]) -> dict[str, Any] | None:
        async with semaphore:
            try:
                data = (
                    _minimal_building_data()
                    if collector is None
                    else await collector(_address_for_point(*point))
                )
                return compute_risk_scores(data)
            except Exception:
                return None

    results = await asyncio.gather(*(assess(point) for point in points))
    valid = [result for result in results if result is not None]
    rating.nb_points_valides = len(valid)
    rating.nb_points_erreur = rating.nb_points - rating.nb_points_valides
    if not valid:
        rating.message = f"0/{rating.nb_points} points evalues"
        return rating

    global_scores = [float(result.get("score_global", 0)) for result in valid]
    rating.score_moyen = statistics.fmean(global_scores)
    rating.score_pondere = rating.score_moyen
    rating.rating_global = _rating_from_mean(rating.score_moyen, max(global_scores))

    peril_scores: dict[str, list[float]] = {}
    for result in valid:
        for name, peril in (result.get("risques_par_alea") or {}).items():
            score = peril.get("risque") if isinstance(peril, dict) else None
            if isinstance(score, (int, float)):
                peril_scores.setdefault(name, []).append(float(score))
    rating.perils = {name: _distribution(scores) for name, scores in peril_scores.items()}
    if rating.perils:
        rating.worst_case_peril, worst = max(
            ((name, peril.worst_case) for name, peril in rating.perils.items()),
            key=lambda item: item[1],
        )
        rating.worst_case_score = worst
    rating.message = f"{rating.nb_points_valides}/{rating.nb_points} points evalues"
    return rating
