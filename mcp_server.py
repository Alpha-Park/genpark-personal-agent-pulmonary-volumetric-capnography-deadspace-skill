"""
MCP Server for Pulmonary Volumetric Capnography Dead Space Skill.
Provides standard Model Context Protocol JSON-RPC tool endpoints.
"""

import sys
import json
from client import VolumetricCapnographyClient


def main():
    client = VolumetricCapnographyClient()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "evaluate_volumetric_capnography",
                            "description": "Calculates Fowler Anatomical Dead Space (Vd_anat), Physiological Dead Space Fraction (Vd/Vt), Alveolar Dead Space (Vd_alv), and Phase III Alveolar Slope (S3) via volumetric capnography.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "tidal_volume_ml": {
                                        "type": "number",
                                        "description": "Expired tidal volume Vt in mL."
                                    },
                                    "arterial_pco2_mmhg": {
                                        "type": "number",
                                        "description": "Arterial PaCO2 in mmHg."
                                    },
                                    "mixed_expired_pco2_mmhg": {
                                        "type": "number",
                                        "description": "Mixed expired mean PCO2 in mmHg."
                                    },
                                    "end_tidal_pco2_mmhg": {
                                        "type": "number",
                                        "description": "Peak end-tidal PetCO2 in mmHg."
                                    },
                                    "fowler_inflection_volume_ml": {
                                        "type": "number",
                                        "description": "Fowler anatomical dead space volume in mL."
                                    },
                                    "phase3_slope_mmhg_per_l": {
                                        "type": "number",
                                        "description": "Phase III alveolar plateau slope in mmHg/L."
                                    }
                                },
                                "required": [
                                    "tidal_volume_ml",
                                    "arterial_pco2_mmhg",
                                    "mixed_expired_pco2_mmhg",
                                    "end_tidal_pco2_mmhg",
                                    "fowler_inflection_volume_ml",
                                    "phase3_slope_mmhg_per_l"
                                ]
                            }
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "evaluate_volumetric_capnography":
                try:
                    out = client.evaluate_volumetric_capnography(**args)
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(out, indent=2)}]
                        }
                    }
                except Exception as e:
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "isError": True,
                        "error": {"code": -32000, "message": str(e)}
                    }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
