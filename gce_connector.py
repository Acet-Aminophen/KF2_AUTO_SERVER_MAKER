from libcloud.compute.types import Provider
import libcloud.compute.providers as prov
from libcloud.compute.types import NodeState


def get_driver(id_is: str, pwd_path: str, project_name: str):
    ce = prov.get_driver(Provider.GCE)
    return ce(id_is, pwd_path, project=project_name)


def get_node(driver: str, name: str):
    return driver.ex_get_node(name)


def get_node_state(driver: str, name: str):
    return str(get_node(driver, name).state)
