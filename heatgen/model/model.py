__author__ = 'baohua'

import os
import sys

from heatgen.template.template import Template
from heatgen.resource.net import Net
from heatgen.resource.middlebox import TransparentMiddleBoxOneArm, TransparentMiddleBoxTwoArm, \
    RoutedMiddleBoxOneArm, RoutedMiddleBoxTwoArm
from heatgen.resource.policy import NodeRef, Policy, ServiceList
from heatgen.mapping.openstack import client
from heatgen.util.log import info, error

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
        self.client = client
        self.version = version
        self.desc = desc
        self.src_id = self.client.get_network_id_by_name(src)
        self.dst_id = self.client.get_network_id_by_name(dst)
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
                mb = self.gen_transparent_mb(e, reverse)
            elif mb_mode == 'routed':
                mb = self.gen_routed_mb(e, reverse)
            else:
                continue
            if not mb:
                error("MB %s cannot generate from cfg file\n" % e)
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

    def gen_transparent_mb(self, name, reverse=False):
        id = get_cfg_value(name,'id') or name
        service_type = get_cfg_value(name,'service_type')
        ingress_node = get_cfg_value(name,'ingress_node')
        ingress_ip = get_cfg_value(name, 'ingress_ip')
        ingress_port = get_cfg_value(name, 'ingress_port') or \
                       self.client.get_ofport_by_ip(ingress_ip)
        if not id or not service_type or not ingress_node or not ingress_port:
            error("gen trans_mb: name=%s,service_type=%s\n" % (name,
                                                             service_type))
            error("IN(node,ip,port)=%s,%s,%s\n" % (ingress_node, ingress_ip,
                                         ingress_port))
            return None
        interface_type = get_cfg_value(name,'interface_type')
        if interface_type == 'one_arm':
            return TransparentMiddleBoxOneArm(id,name,ingress_node,ingress_port,
                                              service_type=service_type)
        else:
            egress_node = get_cfg_value(name,'egress_node')
            egress_ip = get_cfg_value(name, 'egress_ip')
            egress_port = get_cfg_value(name, 'egress_port') or \
                      self.client.get_ofport_by_ip(egress_ip)
            if not egress_node or not egress_port:
                error("OUT(node,ip,port)=%s,%s,%s\n" % (egress_node, egress_ip,
                                                    egress_port))
                return None
            return TransparentMiddleBoxTwoArm(id,name,ingress_node,ingress_port,
                                              egress_node,egress_port,
                                              service_type=service_type)

    def gen_routed_mb(self, name, reverse=False):
        id = get_cfg_value(name,'id') or name
        interface_type = get_cfg_value(name, 'interface_type')
        service_type = get_cfg_value(name,'service_type')
        ingress_gw_addr = get_cfg_value(name,'ingress_gw_addr')
        ingress_cidr = get_cfg_value(name,'ingress_cidr')
        ingress_ip = ingress_cidr[:ingress_cidr.find('/')]
        ingress_mac_addr = get_cfg_value(name, 'ingress_mac_addr') or \
                           self.client.get_mac_by_ip(ingress_ip)
        if not id or not service_type or not ingress_gw_addr or not \
                ingress_cidr or not ingress_mac_addr:
            error("gen routed_mb: name=%s,service_type=%s\n" % (name,
                                                               service_type))
            error("IN(gw,cidr,mac)=%s,%s,%s\n" % (ingress_gw_addr,
                                                   ingress_cidr,
                                                   ingress_mac_addr))
            return None
        if interface_type != 'one_arm':
            egress_gw_addr = get_cfg_value(name,'egress_gw_addr')
            egress_cidr = get_cfg_value(name,'egress_cidr')
            egress_ip = egress_cidr[:egress_cidr.find('/')]
            egress_mac_addr = get_cfg_value(name, 'egress_mac_addr') or \
                              self.client.get_mac_by_ip(egress_ip)
            if not egress_gw_addr or not egress_cidr or not egress_mac_addr:
                error("OUT(node,cidr,mac)=%s,%s,%s\n" % (egress_gw_addr,
                                                         egress_cidr,
                                                         egress_mac_addr))
                return None
        if reverse and interface_type=='two_arm':
            id += '_reverse'
            name += '_reverse'
        if interface_type == 'one_arm':
            return RoutedMiddleBoxOneArm(id, name,
                                         ingress_gw_addr=ingress_gw_addr,
                                         ingress_mac_addr=ingress_mac_addr,
                                         ingress_cidr=ingress_cidr,
                                         service_type=service_type)
        else:
            return RoutedMiddleBoxTwoArm(id, name,
                                         ingress_gw_addr=ingress_gw_addr,
                                         ingress_mac_addr=ingress_mac_addr,
                                         ingress_cidr=ingress_cidr,
                                         egress_gw_addr=egress_gw_addr,
                                         egress_mac_addr=egress_mac_addr,
                                         egress_cidr=egress_cidr,
                                         service_type=service_type)
