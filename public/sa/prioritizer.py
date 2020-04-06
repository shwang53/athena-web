# -*- coding: utf-8 -*-

import time
import sys
import os
import json
import pprint

from athena.summarization.pubsub.prioritizer import Prioritizer
from athena.common.name import Name

pp = pprint.PrettyPrinter(indent=4)
user_id = sys.argv[1]
prefixes = eval(sys.argv[2])

if __name__ == "__main__":    
    with open(os.getenv("HOME")+"/works/athena-web/public/sa/data.json", 'r') as f:
        data = json.load(f)

    selected_names = []    
    for k, v in data.items():
        for prefix in prefixes:
            if Name(prefix).is_prefix_of(Name(k)):
                selected_names.append(k)
                break
    
    p = Prioritizer()        
    infomax_order = p.prioritize(selected_names)['/']

    result = []
    for item in infomax_order:
        result.append([str(Name(item).get_sub_name(0, -2)), str(Name(item).get_name_component(-1)), data[item][0], data[item][1]])

    app_dir = os.getenv("HOME")+"/works/athena-web/users/%s/sa" % user_id
    if not os.path.exists(app_dir):    
        os.system('mkdir -p '+app_dir)

    os.system('rm %s/*' % (app_dir))
    with open(app_dir+"/sorted_list.json", 'w') as f:
        json.dump(result, f)

    print("/users/%s/sa/sorted_list.json" % (user_id))