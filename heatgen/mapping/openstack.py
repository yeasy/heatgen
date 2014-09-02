__author__ = 'baohua'

import sys
from subprocess import Popen, PIPE

from keystoneclient.v2_0 import client as ksclient
from neutronclient.v2_0 import client as neutron_client
from novaclient.v3 import client as nova_client
from oslo.config import cfg

from heatgen.util.log import info, warn

from heatgen.util import config


class Client(object):
    """
    The client to communicate with openstack db to obtain information.
    """

    def __init__(self):
        CONF = cfg.CONF
        config.init(sys.argv[1:])
        self.keystone = ksclient.Client(auth_url=CONF.ADMIN.auth_url,
                                        username=CONF.ADMIN.username,
                                        password=CONF.ADMIN.password,
                                        tenant_name=CONF.ADMIN.tenant_name)
        self.auth_token = self.keystone.auth_token
        self.neutron = neutron_client.Client(auth_url=CONF.PROJECT.auth_url,
                                             username=CONF.PROJECT.username,
                                             password=CONF.PROJECT.password,
                                             tenant_name=CONF.PROJECT.tenant_name)
        self.nova = nova_client.Client(auth_url=CONF.PROJECT.auth_url,
                                       username=CONF.PROJECT.username,
                                       password=CONF.PROJECT.password,
                                       project_id=CONF.PROJECT.tenant_name,
                                       service_type="compute")
        self.CONF = CONF

    """
    Get the OS tenant id by given name.
    """
    def get_tenant_id_by_name(self, name):
        if name:
            for t in self.keystone.tenants.list():
                if t.name == name:
                    return t.id
        return None

    """
    Get the OS network id by given name.
    """
    def get_network_id_by_name(self, name):
        if name:
            for t in self.neutron.list_networks().get('networks'):
                if t['name'] == name:
                    return t['id']
        return None

    """
    Get the port mac by given ip.
    """
    def get_mac_by_ip(self, ip):
        if ip:
            # for s in self.nova.servers.list():
            #    print s.interface_list()
            for p in self.neutron.list_ports().get('ports'):
                if p['tenant_id'] == self.get_tenant_id_by_name(
                        self.CONF.PROJECT.tenant_name):
                    for fix_ip in p['fixed_ips']:
                        if fix_ip.get('ip_address') == ip:
                            return p['mac_address']
        return None

    """
    Get the port id by given ip.
    """

    def get_port_id_by_ip(self, ip):
        if ip:
            # for s in self.nova.servers.list():
            # print s.interface_list()
            for p in self.neutron.list_ports().get('ports'):
                if p['tenant_id'] == self.get_tenant_id_by_name(
                        self.CONF.PROJECT.tenant_name):
                    for fix_ip in p['fixed_ips']:
                        if fix_ip.get('ip_address') == ip:
                            info('Get port id=%s for ip=%s' % (p['id'], ip))
                            return p['id']
        warn('Cannot get port id for ip=%s' % (ip))
        return None

    """
    Get the of port number by given ip.
    """
    def get_ofport_by_ip(self, ip):
        """
        Return the of port number by given ip by checking ovs-ofctl show br
        :param ip:
        :return: None if not found
        """
        port_id = self.get_port_id_by_ip(ip)
        if not port_id:
            warn('Port Id not found')
            return None
        result, error = Popen('ssh %s "ovs-ofctl show br-int"' %
                              self.CONF.compute_node, stdout=PIPE,
                              stderr=PIPE, shell=True).communicate()
        if error:
            return None
        for e in result.split('\n'):
            if port_id[:11] in e:
                port = e[:e.find('(')].strip()
                if str.isdigit(port):
                    return port
        return None


client = Client()
