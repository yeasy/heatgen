__author__ = 'baohua'

from gettext import gettext as _

from oslo.config import cfg
from heatgen import VERSION


default_opts = [
    cfg.StrOpt('src',
               default='',
               help='name of the src endpoint for the policy'),
    cfg.StrOpt('dst',
               default='',
               help='name of the dst endpoint for the policy'),
    cfg.ListOpt('services',
                default=[],
                help='names of the service middleboxes for the policy'),
    cfg.BoolOpt('deploy',
                default=False,
                help='Whether to deploy the rules after generation'),
    cfg.StrOpt('policy_name',
               default='p_policy.json',
               help='name of the exported file for the policy'),
    cfg.BoolOpt('bidirectional',
                default=False,
                help=_("whether add policies in both way")),
    cfg.StrOpt('sdn_controller',
               default='127.0.0.1',
               help='IP address of the sdn controller'),
    cfg.StrOpt('compute_node',
               default='127.0.0.1',
               help='IP address of the compute node'),
]
cfg.CONF.register_cli_opts(default_opts)
cfg.CONF.register_opts(default_opts)

admin_opts = [
    cfg.StrOpt('auth_url',
               default='http://127.0.0.1:5000/v2.0',
               help='authentication url in keystone'),
    cfg.StrOpt('username',
               default='admin',
               help='username in keystone'),
    cfg.StrOpt('password',
               default='admin',
               help='username in keystone'),
    cfg.StrOpt('tenant_name',
               default='admin',
               help='the tenant name to check'),
]
cfg.CONF.register_cli_opts(admin_opts, "ADMIN")
cfg.CONF.register_cli_opts(admin_opts, "PROJECT")
cfg.CONF.register_opts(admin_opts, "ADMIN")
cfg.CONF.register_opts(admin_opts, "PROJECT")

trans_mb_opts = [
    cfg.StrOpt('id',
                default='',
                help=_("id of the middlebox instance")),
    cfg.StrOpt('service_type',
               default='firewall',
               choices=['firewall','ips'],
               help=_("type of the middlebox instance")),
    cfg.StrOpt('mode',
               default='transparent',
               choices=['transparent','routed'],
               help=_("mode of the middlebox instance")),
    cfg.StrOpt('ha_mode',
               default='NONE',
               help=_("the mode for HA")),
    cfg.StrOpt('interface_type',
               choices=['one_arm', 'two_arm'],
               help=_("the type of interface")),
    cfg.StrOpt('required',
               default='no',
               help=_("whether the middlebox instance is required")),
    cfg.BoolOpt('health_check',
                default=False,
                help=_("whether do the health check")),
    cfg.StrOpt('ingress_node',
               default='',
               help=_("ingress switch dpid for the middlebox instance")),
    cfg.StrOpt('ingress_ip',
               default='',
               help=_("fake field to get port of the transparent middlebox "
                      "instance")),
    cfg.StrOpt('ingress_port',
               default='',
               help=_("ingress switch port for the middlebox instance")),
    cfg.StrOpt('egress_ip',
               default='',
               help=_("fake field to get port of the transparent middlebox "
                      "instance")),
    cfg.StrOpt('egress_node',
               default='',
               help=_("egress switch dpid for the middlebox instance")),
    cfg.StrOpt('egress_port',
               default='',
               help=_("egress switch port for the middlebox instance")),
]

routed_mb_opts = [
    cfg.StrOpt('id',
                default='',
                help=_("id of the middlebox instance")),
    cfg.StrOpt('service_type',
               default='firewall',
               choices=['firewall','ips'],
               help=_("type of the middlebox instance")),
    cfg.StrOpt('mode',
               default='transparent',
               choices=['transparent','routed'],
               help=_("mode of the middlebox instance")),
    cfg.StrOpt('ha_mode',
               default='NONE',
               help=_("the mode for HA")),
    cfg.StrOpt('interface_type',
               choices=['one_arm', 'two_arm'],
               help=_("the type of interface")),
    cfg.StrOpt('required',
               default='no',
               help=_("whether the middlebox instance is required")),
    cfg.BoolOpt('health_check',
                default=False,
                help=_("whether do the health check")),
    cfg.StrOpt('ingress_gw_addr',
               default='',
               help=_("ingress gateway ip for the middlebox instance")),
    cfg.StrOpt('ingress_mac_addr',
               default='',
               help=_("ingress mac addr for the middlebox instance")),
    cfg.StrOpt('ingress_cidr',
               default='',
               help=_("ingress ip cidr for the middlebox instance")),
    cfg.StrOpt('egress_gw_addr',
               default='',
               help=_("egress gateway ip for the middlebox instance")),
    cfg.StrOpt('egress_mac_addr',
               default='',
               help=_("egress mac addr for the middlebox instance")),
    cfg.StrOpt('egress_cidr',
               default='',
               help=_("egress ip cidr for the middlebox instance")),
]

cfg.CONF.register_cli_opts(trans_mb_opts, 'trans_mb')
cfg.CONF.register_opts(trans_mb_opts, 'trans_mb')
cfg.CONF.register_cli_opts(routed_mb_opts, 'routed_mb')
cfg.CONF.register_opts(routed_mb_opts, 'routed_mb')

def init(args, **kwargs):
    cfg.CONF(args=args, project='heatgen',
             version='%%prog %s' % VERSION,
             **kwargs)
