from itertools import islice
from datetime import datetime
from twokenize import tokenizeRawTweetText
import numpy as np
from csv import DictReader
import re

def twaggregate(fname, startLine, endLine):
    
    with open(fname, "r") as myfile:
        rawSet = list(islice(myfile, startLine, endLine))
    
    records = []
    rejected = 0
    # index = ['name','party','chamber','time_utc','tweet']
    
    # Process from CSV
    for line in rawSet:
        line = line.strip().lower()
        # name, party, chamber, time, tweet 
        #print line
        record = line.split(',',4)
        #print record
        # Note that some tweets have carriage returns and are broken onto separate lines
        # if len(record)==5:
        if 1==1:
            try: 
                datetime.strptime(record[3], "%Y-%m-%dT%H:%M:%S")
            except (ValueError, IndexError):
                #print "Error on: " + str(record)
                rejected += 1
            else:
                records.append(record)
                        
    # Parse time stamps
    for record in records:
        timestamp = record[3]
        #print timestamp
        # timevec = [int(t) for t in re.split('-|T|:',timestamp)]
        timeformatted = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        #print timeformatted
        record[3] = timeformatted
    
    # Generate daylabels
    for record in records:
        record.append(str(record[3].year)+'.'+str(record[3].month)+'.'+str(record[3].day))
    
    # Generate monthlabels
    for record in records:
        record.append(str(record[3].year)+'.'+str(record[3].month))
    
    # Generate unique value indices
    authors = [i for i in set([record[0] for record in records])]
    #print np.shape(authors)
    parties = [i for i in set([record[1] for record in records])]
    chambers = [i for i in set([record[2] for record in records])]
    days = [i for i in set([record[5] for record in records])]
    months = [i for i in set([record[6] for record in records])]
 
    
    # Aggregate on author, month:
    # Generate key values for aggregation
    keyVals = []
    for author in authors:
        for month in months:
            keyVals.append(author+':'+month) 
    #print "keywals is", keyVals
    
    # Perform aggregation
    twaggregated = {key : "" for key in keyVals}
    #print twaggregated
    for record in records:
        try:
            # ensure tokenize can handle encoding
            tweet = tokenizeRawTweetText(record[4])
            #print tweet
            # try unicode conversion to make sure gensim can handle it
            [unicode(t, encoding='utf8', errors='strict') for t in tweet]
        except: #UnicodeDecodeError
            # print "Token not added. Twokenize error on: " + record[4]
            rejected += 1
        else:
            twaggregated[record[0]+':'+record[6]] += " " + record[4]
    #print "records is", records
    #print np.shape(records)
    #print np.shape(twaggregated)
    #print "twaggregated:", twaggregated
    
    
    tweets = []
    labels = []
    for key, twagg in twaggregated.iteritems():    
        if not twagg=="":
            labels.append(key)
            tweets.append(twagg)
    #print "shape of tweet:", np.shape(tweets)
    return tweets, labels, rejected 
   
def clean(f):
  try:
    return " ".join(re.findall(r'\w+',f,flags = re.UNICODE | re.LOCALE)).lower()
  except:
    return "not_a_valid_value"

                
tweets, labels, rejected = twaggregate("congress.csv", 1, 20000) 
with open("text.txt","wb") as outfile:
    for tweet in tweets:    
        outfile.write("| %s\n" % clean(tweet))     
