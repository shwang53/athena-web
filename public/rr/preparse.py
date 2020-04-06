# -*- coding: utf-8 -*-

import time
import os
import sys
import json
import pprint

from athena.summarization.logic.athena_parser import AthenaParser
from athena.common.name import Name

if __name__ == "__main__":        

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/labels.ath", "r") as f:
        input_str = f.read()

    input_str += "\n"

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/decision.ath", "r") as f:
        input_str += f.read()

    # print(input_str)

    a = AthenaParser()
    result = a.load(input_str)

    with open('decision_tree.ath', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    with open('decision_tree2.ath', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    human_scenario = json.dumps(result, indent=4, ensure_ascii=False).replace('vision_algo', 'human')
    with open('decision_tree1.ath', 'w', encoding='utf-8') as f:
        f.write(human_scenario)    

    decision = dict()    
    labels = dict()
    for k, v in result.items():
        if v[0] == "DECISION":
            decision[k] = v
        else:
            labels[k] = v

    with open('decision_tree3.ath', 'w', encoding='utf-8') as f:
        json.dump(decision, f, indent=4, ensure_ascii=False)    

    with open('decision_tree4.ath', 'w', encoding='utf-8') as f:
        json.dump(labels, f, indent=4, ensure_ascii=False)    

