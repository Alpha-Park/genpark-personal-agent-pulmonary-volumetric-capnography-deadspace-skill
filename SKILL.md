---
name: genpark-personal-agent-pulmonary-volumetric-capnography-deadspace-skill
version: 1.0.0
description: Calculates Fowler Anatomical Dead Space (Vd_anat), Physiological Dead Space Fraction (Vd/Vt), Alveolar Dead Space (Vd_alv), and Phase III Alveolar Slope (S3) via volumetric capnography.
authors:
  - GenPark Ecosystem
tags:
  - personal-agent
  - pulmonary
  - capnography
  - dead-space
  - fowler
  - zero-dependency
---

# Pulmonary Volumetric Capnography Dead Space Skill

## Mathematical Formulation

Physiological Dead Space (Bohr-Enghoff equation):

$$\frac{V_D}{V_T} = \frac{PaCO_2 - P_{\bar{E}}CO_2}{PaCO_2}$$

$$V_D = \left(\frac{V_D}{V_T}\right) \times V_T$$

Alveolar dead space (volume of ventilated but unperfused alveoli):

$$V_{D,\text{alv}} = V_D - V_{D,\text{anat}}$$
$$\frac{V_{D,\text{alv}}}{V_T} = \frac{V_D}{V_T} - \frac{V_{D,\text{anat}}}{V_T}$$

Arterial to End-Tidal $CO_2$ gradient:

$$P(a-et)CO_2 = PaCO_2 - PetCO_2$$

## Clinical Interpretation
- **Normal Dead Space Fraction**: $V_D/V_T \in [0.20, 0.35]$, $V_{D,\text{alv}}/V_T < 0.10$, $S_3 \in [5, 18]\text{ mmHg/L}$
- **Mild V/Q Inhomogeneity**: $V_D/V_T \in [0.35, 0.45]$ or $S_3 \in [18, 25]\text{ mmHg/L}$
- **Marked Alveolar Dead Space Expansion**: $V_D/V_T > 0.45$ or $V_{D,\text{alv}}/V_T > 0.15$ (indicative of acute pulmonary embolism, microvascular occlusion, or ARDS)
