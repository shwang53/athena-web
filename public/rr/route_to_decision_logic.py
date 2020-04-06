# -*- coding: utf-8 -*-

import time
import os
import sys
import json
import pprint

from athena.common.name import Name

if __name__ == "__main__":        

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/route_names.json", "r") as f:
        route_names = json.load(f)

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/route_coordinates.json", "r") as f:
        route_coordinates = json.load(f)        

    labels = dict()
    decision_logic = dict()

    for k, v in route_names.items():
        new_v = list(set(v))
        decision_logic[k] = []
        for item in new_v:
            label_name = "/flooded"+str(Name(item).get_sub_name(1,-1))
            if not label_name in labels:
                labels[label_name] = ["vision_algo", [], "[[%s]]" % (item)]
            decision_logic[k].append("(%s == False)" % (label_name))

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/labels.ath", "w", encoding='utf8') as f:
        for k, v in labels.items():
            f.write("%s = Label(%s, %s, %s)\n" % (k, v[0], v[1], v[2]))

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/decision.ath", "w", encoding='utf8') as f:
        f.write("/viable_route/StaréMěsto/MaláStrana = Decision({\n")
        for k, v in decision_logic.items():
            f.write('\t"%s": %s,\n' % (k, " & ".join(v)))
        f.write('\t"No viable route": otherwise\n})')