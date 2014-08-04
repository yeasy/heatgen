__author__ = 'baohua'

import os
import sys

from template.template import Template
from resource.net import Net
from resource.middlebox import TransparentMiddleBox, RoutedMiddleBox
from resource.policy import NodeRef, Policy, ServiceList
from mapping.openstack import client

def get_cfg_value(group, key):
    from oslo.config import cfg

    try:
        value = eval("cfg.CONF.%s.%s" % (group, key))
        return value
    except cfg.Error:
        print "Error when parsing %s.%s from the cfg file." % (group, key)
        return None


class Model(object):
    """
    The basic class to define a template using high level model
    """

    def __init__(self, version="0.1", desc="Example", src="net1", dst="net2",
                 services=['trans_mb','routed_mb'], policy_name="testpolicy"):
    #node names
        self.version = version
        self.desc = desc
        self.src_id = client.get_network_id_by_name(src)
        self.dst_id = client.get_network_id_by_name(dst)
        self.services = services
        self.resources = []
        self.policy_name = policy_name

    def get_template(self, reverse=False):
        self.resources.append(Net(self.src_id))
        self.resources.append(Net(self.dst_id))
        service_list = ServiceList()
        for e in self.services:
            mb_mode = get_cfg_value(e,'mode')
            if mb_mode == 'transparent':
                mb = self.gen_transparent_mb(e)
            elif mb_mode == 'routed':
                mb = self.gen_routed_mb(e,reverse)
            else:
                continue
            if not mb:
                print "mb %s cannot generate from cfg file" % e
                return None
            if not reverse:
                service_list.add(mb.id)
            else:
                service_list.insert(0, mb.id)
            self.resources.append(mb)
        if not reverse:
            policy = Policy('p_test_id',self.policy_name, NodeRef(self.src_id),
                        NodeRef(self.dst_id), service_list)
        else:
            policy = Policy('p_test_id',self.policy_name+'_reverse', NodeRef(
                self.dst_id), NodeRef(self.src_id), service_list)
        self.resources.append(policy)
        self.template = Template(resources = self.resources)
        return self.template

    def gen_transparent_mb(self, name):
        id = get_cfg_value(name,'id') or name
        service_type = get_cfg_value(name,'service_type')
        ingress_node = get_cfg_value(name,'ingress_node')
        ingress_port = get_cfg_value(name,'ingress_port')
        egress_node = get_cfg_value(name,'egress_node')
        egress_port = get_cfg_value(name,'egress_port')
        if not id or not service_type or not ingress_node or not ingress_port \
                or not egress_node or not egress_port:
            return None
        interface_type = get_cfg_value(name,'interface_type')
        if not interface_type:
            if ingress_node == egress_node and ingress_port == egress_port:
                interface_type = 'one_arm'
            else:
                interface_type = 'two_arm'
        return TransparentMiddleBox(id,name,ingress_node,ingress_port,
                                    egress_node,egress_port, interface_type =\
               interface_type,service_type=service_type)

    def gen_routed_mb(self, name, reverse=False):
        id = get_cfg_value(name,'id') or name
        service_type = get_cfg_value(name,'service_type')
        ingress_gw_addr = get_cfg_value(name,'ingress_gw_addr')
        ingress_cidr = get_cfg_value(name,'ingress_cidr')
        ingress_ip = ingress_cidr[:ingress_cidr.find('/')]
        ingress_mac_addr = get_cfg_value(name, 'ingress_mac_addr') or \
                           client.get_mac_by_ip(ingress_ip)
        egress_gw_addr = get_cfg_value(name,'egress_gw_addr')
        egress_cidr = get_cfg_value(name,'egress_cidr')
        egress_ip = egress_cidr[:egress_cidr.find('/')]
        egress_mac_addr = get_cfg_value(name, 'egress_mac_addr') or \
                          client.get_mac_by_ip(egress_ip)
        if not id or not service_type or not ingress_gw_addr or not \
                ingress_cidr or not ingress_ip or \
                not ingress_mac_addr or not egress_gw_addr or not \
                egress_cidr or not egress_ip or not egress_mac_addr:
            return None
        interface_type = get_cfg_value(name, 'interface_type')
        if not interface_type:
            if ingress_mac_addr == egress_mac_addr:
                interface_type = 'one_arm'
            else:
                interface_type = 'two_arm'
        if not reverse:
            return RoutedMiddleBox(id, name, ingress_gw_addr=ingress_gw_addr,
                               ingress_mac_addr=ingress_mac_addr,
                               ingress_cidr=ingress_cidr,
                               egress_gw_addr=egress_gw_addr,
                               egress_mac_addr=egress_mac_addr,
                               egress_cidr=egress_cidr, interface_type =
            interface_type, service_type=service_type)
        else:
            return RoutedMiddleBox(id+'_reverse', name+'_reverse',
                                   ingress_gw_addr=egress_gw_addr,
                                   ingress_mac_addr=egress_mac_addr,
                                   ingress_cidr=egress_cidr,
                                   egress_gw_addr=ingress_gw_addr,
                                   egress_mac_addr=ingress_mac_addr,
                                   egress_cidr=ingress_cidr, interface_type =
                interface_type, service_type=service_type)