__author__ = 'baohua'

import os
import subprocess
import sys

from oslo.config import cfg

from model import Model
from mapping.openstack import Client


# Fix setuptools' evil madness, and open up (more?) security holes
if 'PYTHONPATH' in os.environ:
    sys.path = os.environ['PYTHONPATH'].split(':') + sys.path

# --config-dir etc
if __name__ == "__main__":
    try:
        CONF = cfg.CONF
        CONF(sys.argv[1:])
        client = Client()
        model = Model(src=CONF.src, dst=CONF.dst, services=CONF.services,
                      policy_name=CONF.policy_name)
        template = model.get_template()
        if not template:
            print "Generate template file error"
            exit(-1)
        file_export = 'p_trans_routed.json'
        print 'Export template to %s' % file_export
        template.export(file_export)
        print 'Deploy the generated template %s' % file_export
        tenant_id = client.get_tenant_id_by_name(CONF.PROJECT.tenant_name)
        deploy_cmd = 'curl -k -u  "admin:admin" -H "multipart/form-data" -F ' \
                     '"templateName=test_template" -F "tenantId=%s" -F ' \
                     '"templateFile=@%s" ' \
                     'https://%s:8443/controller/nb/v2/waypoint/template' \
                     '/import' %(tenant_id, file_export, CONF.sdn_controller)
        if tenant_id and file_export and CONF.sdn_controller:
            p = subprocess.Popen(deploy_cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT).communicate()
            if p[1]:
                print p[1]
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
