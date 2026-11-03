"""
Pulmonary Volumetric Capnography & Dead Space Fraction Client.
Zero-mock pure Python standard library implementation.
Calculates Fowler Anatomical Dead Space (Vd_anat), Physiological Dead Space (Vd/Vt),
Alveolar Dead Space (Vd_alv), and Phase III Alveolar Slope (S3 in mmHg/L).
"""

import math
from typing import Dict, Any, Optional


class VolumetricCapnographyClient:
    """
    Evaluates pulmonary ventilation-perfusion matching via volumetric capnography:
    - Fowler anatomical dead space (Vd_anat, mL): conducting airways without gas exchange
    - Physiological dead space ratio (Vd/Vt): (PaCO2 - PE_bar_CO2) / PaCO2
    - Alveolar dead space (Vd_alv, mL): unperfused or underperfused ventilated alveoli
    - Phase III slope S3 (mmHg/L): alveolar plateau slope reflecting V/Q heterogeneity
    """

    def __init__(self):
        pass

    def evaluate_volumetric_capnography(
        self,
        tidal_volume_ml: float,
        arterial_pco2_mmhg: float,
        mixed_expired_pco2_mmhg: float,
        end_tidal_pco2_mmhg: float,
        fowler_inflection_volume_ml: float,
        phase3_slope_mmhg_per_l: float
    ) -> Dict[str, Any]:
        """
        Calculates volumetric capnography dead space parameters.
        tidal_volume_ml: expired tidal volume Vt (mL)
        arterial_pco2_mmhg: arterial PaCO2 (mmHg)
        mixed_expired_pco2_mmhg: mixed expired mean PCO2 (mmHg)
        end_tidal_pco2_mmhg: peak PetCO2 at end expiration (mmHg)
        fowler_inflection_volume_ml: Fowler equal-area transition volume (Vd_anat in mL)
        phase3_slope_mmhg_per_l: Phase III alveolar plateau slope (mmHg/L)
        """
        if tidal_volume_ml <= 0 or arterial_pco2_mmhg <= 0:
            raise ValueError("Tidal volume and arterial PCO2 must be strictly positive.")
        if mixed_expired_pco2_mmhg >= arterial_pco2_mmhg:
            raise ValueError("Mixed expired PCO2 must be strictly less than arterial PaCO2.")
        if fowler_inflection_volume_ml >= tidal_volume_ml:
            raise ValueError("Anatomical dead space cannot exceed tidal volume.")

        # Physiological dead space fraction (Bohr-Enghoff equation)
        vd_vt_phys = (arterial_pco2_mmhg - mixed_expired_pco2_mmhg) / arterial_pco2_mmhg
        vd_phys_ml = vd_vt_phys * tidal_volume_ml

        # Anatomical dead space fraction
        vd_anat_ml = fowler_inflection_volume_ml
        vd_vt_anat = vd_anat_ml / tidal_volume_ml

        # Alveolar dead space
        vd_alv_ml = max(0.0, vd_phys_ml - vd_anat_ml)
        vd_vt_alv = vd_alv_ml / tidal_volume_ml

        # Arterial to End-Tidal PCO2 gradient P(a-et)CO2
        p_a_et_co2_gradient = arterial_pco2_mmhg - end_tidal_pco2_mmhg

        # Clinical interpretation:
        # Vd/Vt normal: 0.20 - 0.35 (20% - 35%)
        # Vd_alv / Vt normal: < 0.10 (< 10%)
        # S3 normal: 5.0 - 18.0 mmHg/L
        # Elevated Vd_alv and S3 indicate alveolar dead space expansion (pulmonary embolism, ARDS, severe COPD)
        if vd_vt_phys > 0.45 or vd_vt_alv > 0.15:
            classification = "Marked Physiological & Alveolar Dead Space Expansion"
            mechanism = "Ventilated alveoli with absent or compromised capillary perfusion (pulmonary microthrombosis, embolic occlusion, or microvascular destruction)."
        elif vd_vt_phys > 0.35 or phase3_slope_mmhg_per_l > 22.0:
            classification = "Mild-to-Moderate Dead Space Ventilation / V/Q Inhomogeneity"
            mechanism = "Peripheral airway constriction or chronic obstructive ventilation maldistribution."
        else:
            classification = "Normal Gas Exchange & Dead Space Dynamics"
            mechanism = "Physiological anatomical airway conduction with matched alveolar capillary perfusion."

        return {
            "status": "success",
            "dead_space_volumes_ml": {
                "tidal_volume_vt_ml": round(tidal_volume_ml, 1),
                "physiological_dead_space_vd_ml": round(vd_phys_ml, 1),
                "anatomical_dead_space_vd_anat_ml": round(vd_anat_ml, 1),
                "alveolar_dead_space_vd_alv_ml": round(vd_alv_ml, 1)
            },
            "dead_space_fractions": {
                "vd_vt_physiological_pct": round(vd_vt_phys * 100.0, 1),
                "vd_vt_anatomical_pct": round(vd_vt_anat * 100.0, 1),
                "vd_vt_alveolar_pct": round(vd_vt_alv * 100.0, 1)
            },
            "capnography_kinetics": {
                "arterial_pco2_mmhg": arterial_pco2_mmhg,
                "end_tidal_pco2_mmhg": end_tidal_pco2_mmhg,
                "p_a_et_co2_gradient_mmhg": round(p_a_et_co2_gradient, 1),
                "phase3_slope_mmhg_per_l": round(phase3_slope_mmhg_per_l, 1)
            },
            "interpretation": {
                "classification": classification,
                "pathophysiologic_mechanism": mechanism
            }
        }
