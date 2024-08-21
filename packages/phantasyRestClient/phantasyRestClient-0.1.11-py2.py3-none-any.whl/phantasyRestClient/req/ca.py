#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Request for resources from ca (Channel Access) router.
"""
import json
from typing import List, Union


class CAResources:
    SESSION = None
    URL = None

    def __init__(self):
        pass

    @staticmethod
    def caget(pvname: Union[List[str], str], datatype: str = None):
        """Return the values of a list of PVs, if only one string of
        PV is passed, return a single value.
        """
        r = CAResources.SESSION.post(
            f"{CAResources.URL}/epics/caget",
            data=json.dumps(pvname),
            params={'datatype': datatype})
        if not r.ok:
            return None
        return r.json()
