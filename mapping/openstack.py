__author__ = 'baohua'

import config  # noqa
from keystoneclient.v2_0 import client as ksclient
from neutronclient.v2_0 import client as neutron_client
from novaclient.v3 import client as nova_client
from oslo.config import cfg


class Client(object):
    """
    The client to communicate with openstack db to obtain information.
    """

    def __init__(self):
        CONF = cfg.CONF
        #CONF(sys.argv[1:])
        self.keystone = ksclient.Client(auth_url=CONF.AUTH.auth_url,
                                        username=CONF.AUTH.username,
                                        password=CONF.AUTH.password,
                                        tenant_name=CONF.AUTH.tenant_name)
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

    def get_tenant_id_by_name(self, name):
        if name:
            for t in self.keystone.tenants.list():
                if t.name == name:
                    return t.id
        return None

    def get_network_id_by_name(self, name):
        if name:
            for t in self.neutron.list_networks().get('networks'):
                if t['name'] == name:
                    return t['id']
        return None

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


client = Client()
