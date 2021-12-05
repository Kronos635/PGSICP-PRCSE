#!/usr/bin/env python
# coding: utf-8
#

from LigacaoBD import *


createTables()
resource=("resource1",)
insert_resource(resource)
resource=("resource2",)
insert_resource(resource)
resource=("resource3",)
insert_resource(resource)

list_resource(("ALL",))

insert_resource(resource)

con.close()
