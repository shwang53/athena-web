import os
import sys
import logging
import time
import random
import json
import argparse
import pprint
import random
from threading import Timer, Lock

from athena.summarization.logic.decision_maker import DecisionMaker
from athena.common.name import Name

WEP_APP_DIR = os.getenv("HOME")+"/works/athena-web/public/rr"
pp = pprint.PrettyPrinter(indent=4)

RIVERSIDE = [
    "470b94f6f4",
    "470b94f6d4",
    "470b94f0e4",
    "470b94f00c",
    "470b94f05c",
    "470b94e55c",
    "470b94e57c",
    "470b94e58c",
    "470b94e604",
    "470b94e6fc",
    "470b94dd44",
    "470b94f7cc",
    "470b94f7dc",
    "470b94f77c",
    "470b94f764",
    "470b94f9dc",
    "470b94f9f4",
    "470b94fa24",
    "470b94fa34",
    "470b94fa54",
    "470b94fb04",
    "470b94fb1c",
    "470b94fadc"
]

class RouteFinder(object):

    def __init__(self, user_id, vehicle_weight, source, dest, annotator):
        self.dm = DecisionMaker()           
        self.is_running = False
        self.predicates = dict()
        self.user_id = user_id
        self.source = source
        self.dest = dest

        self.retrieval_cnt = 0
        with open('%s/ground_truth.json' % (WEP_APP_DIR), 'r') as f:
            self.ground_truth = json.load(f)

        if annotator == 1:
            # Human
            self.dm.set_annotate_func(self.human)
            with open('%s/decision_tree1.ath' % (WEP_APP_DIR), 'r') as f:
                variables = json.load(f)            

        elif annotator == 2:
            # Human
            self.dm.set_annotate_func(self.vision_algo)
            with open('%s/decision_tree2.ath' % (WEP_APP_DIR), 'r') as f:
                variables = json.load(f)            

        elif annotator == 3:
            with open('%s/decision_tree3.ath' % (WEP_APP_DIR), 'r') as f:
                variables = json.load(f)

        else:
            print("Undefined annotator type: %s" % (annotator))
            return

        with open(os.getenv("HOME")+"/works/athena-framework/applications/sa-demo/prefix.json", 'r') as f:
            prefix_dict = eval(f.read())    

        prefix_set = set(prefix_dict.keys())        
        # for k, v in prefix_dict.items():
        #     prefix_set |= set(v)

        self.prob = dict()
        decision = variables["/viable_route/%s/%s" % (self.source, self.dest)]
        
        self.prob["/vehicle/weight<10"] = 1.0 if vehicle_weight <= 1 else 0.0
        self.prob["/vehicle/weight<20"] = 1.0 if vehicle_weight <= 2 else 0.0
        self.prob["/vehicle/weight<30"] = 1.0 if vehicle_weight <= 3 else 0.0        

        for k, v in decision[3].items():        
            if ''.join(v) in self.prob:
                continue
            
            if str(Name(v[0]).get_name_component(-1)) in RIVERSIDE:
                self.prob[''.join(v)] = 0.1
            else:
                self.prob[''.join(v)] = 0.9

            # prefix = "/image"+str(Name(v[0]).get_sub_name(1, -1))
            # for sensor in prefix_set:            
            #     self.prob[''.join(v)] = 1.0
            #     if Name(prefix).is_prefix_of(Name(sensor)):                            
            #         self.prob[''.join(v)] = 0.5
            #         break       

        pp.pprint(self.prob)
        self.dm.load_vars(variables)


    def human(self, args, dataset):    
        self.retrieval_cnt += 1

        data_name = list(dataset.keys())
        request_file = os.getenv("HOME")+"/works/athena-web/users/%s/rr/annotate_request.json"%(self.user_id)
        with open(request_file, 'w') as f:
            json.dump(data_name, f)

        answer_file = os.getenv("HOME")+"/works/athena-web/users/%s/rr/answer.txt"%(self.user_id)
        cnt = 0
        while not os.path.isfile(answer_file):        
            time.sleep(1)
            cnt += 1
            if cnt >= 60:
                return None

        with open(answer_file, 'r') as f:
            value = eval(f.read())
        
        with open(request_file, 'w') as f:
            json.dump([], f)

        os.system("rm %s" % (answer_file))
        return value


    def vision_algo(self, args, dataset):
        self.retrieval_cnt += 1

        return_val = False
        for k, v in dataset.items():
            region = str(Name(k).get_sub_name(1, -3))
            if region in self.ground_truth:
                return_val = True
        
        print("Return %s" % (return_val))        
        return return_val


    def on_decision(self, decision_query, decision, reason):
        self.predicates[decision_query] = decision

        if decision_query == '/viable_route/%s/%s' % (self.source, self.dest):            
            print("Decision on %s is %s because %s" % (decision_query, decision, reason))    
            self.predicates["count"] = self.retrieval_cnt
            self.is_running = False
            self.report()
            self.dm.close()                         


    def run(self):
        self.is_running = True        
        self.report()
        self.dm.decide('/viable_route/%s/%s' % (self.source, self.dest), self.on_decision, prob=self.prob) 


    def report(self):
        with open(os.getenv("HOME")+"/works/athena-web/users/%s/rr/predicates.json"%(self.user_id), 'w', encoding='utf-8') as f:
            json.dump(self.predicates, f, ensure_ascii=False)

        if self.is_running:                        
            Timer(1, self.report).start()        
            

if __name__ == "__main__":
    user_id = sys.argv[1]
    vehicle_weight = int(sys.argv[2])
    source = sys.argv[3]
    dest = sys.argv[4]
    annotator = int(sys.argv[5])

    rf = RouteFinder(user_id, vehicle_weight, source, dest, annotator)
    rf.run()


    