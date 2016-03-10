import os
target = os.path.join(os.path.dirname(__file__),
                      '../opentuner/opentuner/utils/adddeps.py')
execfile(target, dict(__file__=target))

