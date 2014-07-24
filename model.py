__author__ = 'baohua'

import os
import sys

from template.template import Template
from oslo.config import cfg
from resource.net import Net
from resource.middlebox import TransparentMiddleBox, RoutedMiddleBox
from resource.policy import NodeRef, Policy, ServiceList

from mapping import config #noqa

# Fix setuptools' evil madness, and open up (more?) security holes
if 'PYTHONPATH' in os.environ:
    sys.path = os.environ['PYTHONPATH'].split(':') + sys.path


def get_cfg_value(group,key):
    return eval("cfg.CONF.%s.%s" %(group, key))

class Model(object):
    """
    The basic class to define a template using high level model
    """

    def __init__(self, version="0.1", desc="Example", src="net1", dst="net2",
                 services=['trans_mb','routed_mb'], policy_name="testpolicy"):
    #node names
        self.version = version
        self.desc = desc
        self.src = src
        self.dst = dst
        self.services = services
        self.resources = []
        self.policy_name = policy_name

    def get_template(self):
        src_id = get_cfg_value(self.src,'id')
        dst_id = get_cfg_value(self.dst,'id')
        self.resources.append(Net(src_id))
        self.resources.append(Net(dst_id))
        service_list = ServiceList()
        for e in self.services:
            mb_mode = get_cfg_value(e,'mode')
            if mb_mode == 'transparent':
                mb = self.gen_transparent_mb(e)
            elif mb_mode == 'routed':
                mb = self.gen_routed_mb(e)
            else:
                continue
            service_list.add(mb.id)
            self.resources.append(mb)
        policy = Policy('',self.policy_name,NodeRef(src_id),NodeRef(dst_id),service_list)
        self.resources.append(policy)
        self.template = Template(resources = self.resources)
        return self.template

    def gen_transparent_mb(self, name):
        id = get_cfg_value(name,'id')
        service_type = get_cfg_value(name,'service_type')
        ingress_node = get_cfg_value(name,'ingress_node')
        ingress_port = get_cfg_value(name,'ingress_port')
        egress_node = get_cfg_value(name,'egress_node')
        egress_port = get_cfg_value(name,'egress_port')
        if ingress_node == egress_node and ingress_port == egress_port:
            interface_type = 'one_arm'
        else:
            interface_type = 'two_arm'
        return TransparentMiddleBox(id,name,ingress_node,ingress_port,
                                    egress_node,egress_port, interface_type =\
               interface_type)

    def gen_routed_mb(self, name):
        id = get_cfg_value(name,'id')
        service_type = get_cfg_value(name,'service_type')
        ingress_gw_addr = get_cfg_value(name,'ingress_gw_addr')
        ingress_mac_addr = get_cfg_value(name,'ingress_mac_addr')
        ingress_cidr = get_cfg_value(name,'ingress_cidr')
        egress_gw_addr = get_cfg_value(name,'egress_gw_addr')
        egress_mac_addr = get_cfg_value(name,'egress_mac_addr')
        egress_cidr = get_cfg_value(name,'egress_cidr')
        if ingress_mac_addr == egress_mac_addr:
            interface_type = 'one_arm'
        else:
            interface_type = 'two_arm'
        return RoutedMiddleBox(id, name, ingress_gw_addr, ingress_mac_addr,
                               ingress_cidr, egress_gw_addr, egress_mac_addr,
                               egress_cidr, interface_type = interface_type)
