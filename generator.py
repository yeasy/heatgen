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

CONF = cfg.CONF

def gen_template(model, filename='policy.json', reverse=False):
    template = model.get_template(reverse)
    if not template:
        print "Generate template file error"
        return None
    print 'Export template to %s' % filename
    template.export(filename)
    return True

def deploy_template(filename):
    client = Client()
    print 'Deploy the generated template %s' % filename
    tenant_id = client.get_tenant_id_by_name(CONF.PROJECT.tenant_name)
    deploy_cmd = 'curl -k -u  "admin:admin" -H "multipart/form-data" -F ' \
                 '"templateName=test_template" -F "tenantId=%s" -F ' \
                 '"templateFile=@%s" ' \
                 'https://%s:8443/controller/nb/v2/waypoint/template' \
                 '/import' %(tenant_id, filename, CONF.sdn_controller)
    if tenant_id and filename and CONF.sdn_controller:
        p = subprocess.Popen(deploy_cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT).communicate()
        if p[1]:
            print p[1]

def _gen_and_deploy(model, filename='policy.json', reverse=False):
    if reverse:
        filename += '_reverse'
    if gen_template(model, filename, reverse):
        deploy_template(filename)
        pass


def gen_and_deploy(bidirectional=False):
    model = Model(src=CONF.src, dst=CONF.dst, services=CONF.services,
                  policy_name=CONF.policy_name)
    _gen_and_deploy(model)
    if bidirectional:
        _gen_and_deploy(model,reverse=True)

# --config-dir etc
if __name__ == "__main__":
    try:
        CONF(sys.argv[1:])
        gen_and_deploy(CONF.bidirectional)
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
