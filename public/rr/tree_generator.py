# -*- coding: utf-8 -*-

import time
import os
import sys
import json
import pprint
import s2sphere

from athena.common.name import Name

user_id = sys.argv[1]
if __name__ == "__main__":        

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/decision_tree2.ath", "r") as f:
        variables = json.load(f)

    tree = variables["/viable_route/StaréMěsto/MaláStrana"][2]
    new_tree = dict()
    for k, v in tree.items():        
        if v == 'otherwise':
            continue
        v = v.replace('And', '')        
        v = v.replace('(', '')        
        v = v.replace(')', '')
        v = v.replace(' ', '')
        tokens = v.split(",")
        new_tree[eval(k)] = tokens

    app_dir = os.getenv("HOME")+"/works/athena-web/users/%s/rr" % user_id
    if not os.path.exists(app_dir):    
        os.system('mkdir -p '+app_dir)
    os.system('rm %s/*' % (app_dir))

    with open(app_dir+"/decision_tree.json", 'w') as f:
        json.dump(new_tree, f)    

    with open(app_dir+"/predicates.json", 'w') as f:
        json.dump({}, f)
    
    with open(app_dir+"/annotate_request.json", 'w') as f:
        json.dump([], f)

    print("/users/%s/rr" % user_id)


