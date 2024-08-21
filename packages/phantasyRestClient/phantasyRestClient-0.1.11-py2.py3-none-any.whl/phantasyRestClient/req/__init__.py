import requests
from phantasyRestClient.config import conf_dict
from phantasyRestClient.req.mp import MachinePortalResources
from phantasyRestClient.req.ca import CAResources
from phantasyRestClient.req.phy import PhysicsResources

session = requests.Session()
session.verify = False

# mp resources
MachinePortalResources.SESSION = session
MachinePortalResources.URL = conf_dict['bind']

# ca resources
CAResources.SESSION = session
CAResources.URL = conf_dict['bind']

# phy resources
PhysicsResources.SESSION = session
PhysicsResources.URL = conf_dict['bind']
