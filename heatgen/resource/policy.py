__author__ = 'baohua'

import json
from heatgen.resource.resource import Resource


class NodeRef(object):
    """
    A noderef is a ref endpoint for a policy

    >>> print NodeRef("0001").get_json()
    {"Ref": "0001"}
    """

    def __init__(self, ref_id):
        self.ref = ref_id

    def get(self):
        return {"Ref":self.ref}

    def get_json(self):
        return json.dumps(self.get())


class ServiceList(object):
    """
    The class for a list of services, including several ids of middleboxes,
    e.g.,
    """

    def __init__(self, *args):
        self.data = []
        for arg in args:
            self.data.append(NodeRef(arg).get())

    def add(self, mb_id):
        """
        Add a mb at the end.
        """
        self.data.append(NodeRef(mb_id).get())

    def insert(self, pos, mb_id):
        """
        Insert a mb at pos.
        """
        self.data.insert(pos, NodeRef(mb_id).get())

    def get(self):
        return self.data

    def get_json(self):
        return json.dumps(self.get())


class Policy(Resource):
    """
    The class for a policy resource

    >>> print Policy("01","P1",NodeRef("001"),NodeRef("002"),ServiceList("003","004")).get_json()
    {"01": {"Type": "OS::Neutron::policy", "Properties": {"service_list": [{"Ref": "003"}, {"Ref": "004"}], "policy_dest": {"Ref": "002"}, "policy_src": {"Ref": "001"}, "name": "P1", "policy_type": "conn_service"}}}
    """

    def __init__(self, id, name, policy_src, policy_dest, service_list, policy_type="conn_service",
                 type="OS::Neutron::policy"):
        super(Policy,self).__init__(id, type, name=name,
                                    policy_src=policy_src.get(), policy_dest=policy_dest.get(),
                                    service_list=service_list.get(), policy_type=policy_type)


if __name__ == "__main__":
    import doctest
    doctest.testmod()