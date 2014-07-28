__author__ = 'baohua'

from resource import Resource

class MiddleBox(Resource):
    """
    The basic class for a middlebox

    >>> print MiddleBox("01").get_json()
    {"01": {"Type": "OS::Neutron::connectivity::service", "Properties": {"name": "trans_mb", "interface_type": "two_arm", "required": "yes", "ha_mode": "NONE", "mode": "transparent", "service_type": "firewall"}}}
    """

    def __init__(self,id,type="OS::Neutron::connectivity::service", name="trans_mb",
                 interface_type="two_arm", service_type="firewall", ha_mode="NONE",required="yes",
                 mode="transparent",health_check="false",**kwargs):
        super(MiddleBox,self).__init__(id,type,name=name, interface_type=interface_type, service_type=service_type,
                                       ha_mode=ha_mode,required=required, mode=mode,health_check="false", **kwargs)



class TransparentMiddleBox(MiddleBox):
    """
    The class for a transparent middlebox

    >>> print TransparentMiddleBox("1","xgs","00:01","1","00:01","2").get_json()
    {"1": {"Type": "OS::Neutron::connectivity::service", "Properties": {"ingress_port": "1", "interface_type":
    "two_arm", "required": "yes", "egress_port": "2", "egress_node": "00:01", "ingress_node": "00:01", "ha_mode":
    "NONE", "mode": "transparent", "service_type": "ips", "name": "xgs"}}}
    """
    def __init__(self, id, name, ingress_node,ingress_port,egress_node,egress_port,
                 type="OS::Neutron::connectivity::service", interface_type="two_arm", service_type="ips",
                 ha_mode="NONE",required="yes",health_check="false"):
        super(TransparentMiddleBox,self).__init__(id, type, name=name, interface_type=interface_type,
                                                  ingress_node=ingress_node, service_type=service_type,
                                                  ha_mode=ha_mode,
                                                  required=required,
                                                  ingress_port=ingress_port, egress_node=egress_node,
                                                  egress_port=egress_port,
                                                  health_check=health_check,
                                                  mode='transparent')



class RoutedMiddleBox(MiddleBox):
    """
    The class for a transparent middlebox

    >>> print RoutedMiddleBox("1","routed","192.168.1.1","00:01","192.168.1.4/24","192.168.2.1", "00:02",\
    "192.168.2.4/24").get_json()
    {"1": {"Type": "OS::Neutron::connectivity::service", "Properties": {"egress_gw_addr": "192.168.2.1", "name": "routed", "interface_type": "two_arm", "required": "yes", "ingress_cidr": "192.168.1.4/24", "service_type": "firewall", "egress_mac_addr": "00:02", "ingress_gw_addr": "192.168.1.1", "egress_cidr": "192.168.2.4/24", "ha_mode": "NONE", "ingress_mac_addr": "00:01", "mode": "transparent"}}}
    """
    def __init__(self, id, name, ingress_gw_addr, ingress_mac_addr, ingress_cidr, egress_gw_addr,
                 egress_mac_addr, egress_cidr,
                 type="OS::Neutron::connectivity::service", interface_type="two_arm", service_type="firewall",
                 ha_mode="NONE",required="yes",health_check="false"):
        super(RoutedMiddleBox,self).__init__(id, type, name=name, ingress_gw_addr=ingress_gw_addr,
                                             ingress_mac_addr=ingress_mac_addr, ingress_cidr=ingress_cidr,
                                             egress_gw_addr=egress_gw_addr, egress_mac_addr=egress_mac_addr,
                                             egress_cidr=egress_cidr, interface_type=interface_type,
                                             service_type=service_type,
                                             ha_mode=ha_mode,
                                             required=required,
                                             health_check=health_check,
                                             mode='routed' )



if __name__ == "__main__":
    import doctest
    doctest.testmod()
