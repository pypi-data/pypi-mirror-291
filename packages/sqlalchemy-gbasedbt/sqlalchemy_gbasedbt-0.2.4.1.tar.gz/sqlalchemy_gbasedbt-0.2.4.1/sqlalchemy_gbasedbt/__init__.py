__version__ = '0.2.4.1'

import os
from sqlalchemy.dialects import registry

os.environ['DELIMIDENT'] = 'y'

registry.register("gbasedbt", "sqlalchemy_gbasedbt.dbtdb", "GBasedbtDialect")
