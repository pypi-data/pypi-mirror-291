import pytest
from phantasyRestClient import PhysicsResources as phy_res


def test_calcEnergyLoss():
    p = {"A": 238, "Z": 92, "Ek": 1000}
    m = {"A": 63.546, "Z": 29, "thickness": 1000}
    r = phy_res.calcEnergyLoss(p, m)
    r0 = {
        'dE/dx': 14.518020957575775,
        'Ek': 938.6732788085938,
        'Ek_std': 0.28671697408211333,
        'range_in': 12592.18308165448,
        'range_out': 11592.183580096036,
        'range_std': 11.897422600402564,
        'angle_std': 1.0526343248784542,
        'q_in': 91.76187896728516,
        'q_out': 91.74201965332031
    }
    assert r == r0


def test_calcEnergyLossList():
    p = {"A": 238, "Z": 92, "Ek": 1000}
    m = {"A": 63.546, "Z": 29, "thickness": 1000}
    r = phy_res.calcEnergyLossList(p, m)
    r0 = [
        938.6732788085938,
        14.518020957575775,
        0.28671697408211333,
        12592.18308165448,
        11592.183580096036,
        11.897422600402564,
        1.0526343248784542,
        91.76187896728516,
        91.74201965332031
        ]
    assert r == r0
