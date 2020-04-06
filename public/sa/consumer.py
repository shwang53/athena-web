# -*- coding: utf-8 -*-

import sys
from athena.transport.consumer import Consumer

interest_name = sys.argv[1]
c = Consumer()

def on_success(data_name, contents):
    print("Success")
    c.close()

def on_failure(interest_name):
    print("Fail")
    c.close()

def main():    
    c.consume(interest_name, on_success, on_failure)    

if __name__ == "__main__":
    main()
