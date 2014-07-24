__author__ = 'baohua'

import  sys

from oslo.config import cfg
from mapping import config #noqa

from model import Model

if __name__ == "__main__":
    try:
        CONF = cfg.CONF
        CONF(project='heatgen')
        model = Model(src=CONF.src, dst=CONF.dst, services=['trans_mb',
                                                          'routed_mb'],
                      policy_name='policy_test')
        template = model.get_template()
        print template.get_json()
        template.export()
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
