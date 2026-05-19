#!/usr/bin/env python3
# ==============================================================================
# SYSTEM: SSISM / MYISM V5 Matrix
# MODULE: POORMANMEISM_ENGINE_V5.py
# AUTHOR: U Ingar Soe
# PURPOSE: Computes Digital Trust Score (Φ), Processes Atta-Hita/Para-Hita Loop,
#          and Executes the Sculptor's Logic Guardrails.
# ==============================================================================

import math
import sys
import logging

class PoormanmeismV5Engine:
    def __init__(self, authority: float, urgency: float, linguistics: float, anomaly: float):
        self.A = max(0.0, min(1.0, authority))     # Engineered/Top-Down Authority
        self.U = max(0.0, min(1.0, urgency))       # Socially Engineered Urgency
        self.L = max(0.0, min(1.0, linguistics))   # Linguistic Anomaly Vector
        self.dT = max(0.0, min(1.0, anomaly))      # Time Anomaly Vector
        self.LOCKOUT_THRESHOLD = 0.20

    def calculate_total_risk_z(self) -> float:
        w_authority, w_urgency, w_linguistics, w_anomaly = 0.35, 0.30, 0.20, 0.15
        return (w_authority * self.A) + (w_urgency * self.U) + (w_linguistics * self.L) + (w_anomaly * self.dT)

    def evaluate_digital_trust_phi(self) -> float:
        Z = self.calculate_total_risk_z()
        try:
            return 1.0 / (1.0 + math.exp(Z * 5.0 - 2.0))
        except OverflowError:
            return 0.0
          
