#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Request for resources from phy (physics) router.
"""
import json


class PhysicsResources:
    SESSION = None
    URL = None

    def __init__(self):
        pass

    @staticmethod
    def calcEnergyLoss(projectile: dict, material: dict):
        """Calculate energy loss with ATIMA, returns a dict.
        """
        r = PhysicsResources.SESSION.post(
                f"{PhysicsResources.URL}/physics/atima/calc",
                data=json.dumps({
                    "projectile": projectile,
                    "material": material,
                }))
        if not r.ok:
            return None
        return r.json()

    @staticmethod
    def calcEnergyLossList(projectile: dict, material: dict):
        """Calculate energy loss with ATIMA, returns a list.
        """
        r = PhysicsResources.calcEnergyLoss(projectile, material)
        if r is not None:
            return [r[k] for k in ('Ek', 'dE/dx', 'Ek_std',
                                   'range_in', 'range_out',
                                   'range_std', 'angle_std',
                                   'q_in', 'q_out')]
        else:
            return []
