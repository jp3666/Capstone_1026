'''
Created on Oct 22, 2014

@author: jingping
'''

import numpy as np
from csv import DictReader
import re

f = "congress.csv"
train = "congress_train.txt"
  
def clean(f):
  try:
    return " ".join(re.findall(r'\w+',f,flags = re.UNICODE | re.LOCALE)).lower()
  except:
    return "not_a_valid_value"

def main():
  with open("congress_train.txt","wb") as outfile:
    #For every enumerated row {} in csv file
    for e, row in enumerate( DictReader(open(f,"rb"))):
      outfile.write("| %s\n" % clean(row['text']))
      #Report
      if e % 1000 == 0:
        print(e)
    print(e)


main()
a = open("dictnostops.txt")

