"""
Example usage of Pulmonary Volumetric Capnography Dead Space Skill.
Demonstrates normal dead space ventilation vs severe alveolar dead space expansion in pulmonary embolism.
"""

import json
from client import VolumetricCapnographyClient


def main():
    print("=== Testing Pulmonary Volumetric Capnography Skill ===")
    client = VolumetricCapnographyClient()

    # 1. Healthy ventilated subject (Vt=500mL, PaCO2=40mmHg, PE_bar=28mmHg, PetCO2=38mmHg, Vd_anat=140mL -> Vd/Vt=30%, Vd_alv=10mL (2%))
    res_normal = client.evaluate_volumetric_capnography(
        tidal_volume_ml=500.0,
        arterial_pco2_mmhg=40.0,
        mixed_expired_pco2_mmhg=28.0,
        end_tidal_pco2_mmhg=38.0,
        fowler_inflection_volume_ml=140.0,
        phase3_slope_mmhg_per_l=12.0
    )
    print("\n[Case 1: Normal Volumetric Capnography & Dead Space]")
    print(json.dumps(res_normal, indent=2))

    # 2. Patient with massive pulmonary embolism / vascular occlusion (Vt=500mL, PaCO2=46mmHg, PE_bar=20mmHg, PetCO2=26mmHg, Vd_anat=145mL -> Vd/Vt=56.5%, Vd_alv=137.6mL (27.5%))
    res_pe = client.evaluate_volumetric_capnography(
        tidal_volume_ml=500.0,
        arterial_pco2_mmhg=46.0,
        mixed_expired_pco2_mmhg=20.0,
        end_tidal_pco2_mmhg=26.0,
        fowler_inflection_volume_ml=145.0,
        phase3_slope_mmhg_per_l=32.0
    )
    print("\n[Case 2: Severe Alveolar Dead Space Expansion (Pulmonary Embolism)]")
    print(json.dumps(res_pe, indent=2))

    # Assertions
    assert res_normal["dead_space_fractions"]["vd_vt_alveolar_pct"] < 10.0
    assert "Normal" in res_normal["interpretation"]["classification"]
    assert res_pe["dead_space_fractions"]["vd_vt_alveolar_pct"] > 15.0
    assert "Marked" in res_pe["interpretation"]["classification"]
    print("\n[SUCCESS] Volumetric Capnography tests passed!")


if __name__ == "__main__":
    main()
