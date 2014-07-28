__author__ = 'baohua'

import  sys

from oslo.config import cfg

from mapping.openstack import Client
from model import Model

# --config-dir etc
if __name__ == "__main__":
    try:
        CONF = cfg.CONF
        CONF(project='heatgen')
        client = Client()
        # print client.get_tenant_id_by_name(CONF.PROJECT.tenant_name)
        model = Model(src=CONF.src, dst=CONF.dst, services=CONF.services,
                      policy_name=CONF.policy_name)
        template = model.get_template()
        print template.get_json()
        template.export('p_trans_routed.json')
    except ValueError as e:
        # Print exception
        type_, val_, trace_ = sys.exc_info()
        errorMsg = _("-" * 80 + "\n" +
                     "Caught exception. Cleaning up...\n\n" +
                     "%s: %s\n" % (type_.__name__, val_) +
                     "-" * 80 + "\n")
        print errorMsg
        # Print stack trace to debug log
        import traceback
        stackTrace = traceback.format_exc()
        print stackTrace
