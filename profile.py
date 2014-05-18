import pymongo, sys, time, math
client = pymongo.MongoClient()
db = client.sim
coll = db.compounds

nmol = 1000
tcut = 0.9

fpfile = open('fp.txt', 'r')
fpfile.readline()
queries = []
for i in range(0, nmol):
    line = fpfile.readline()
    if line.strip().find(" ") == -1: continue
    molregno, bits = line.strip().split(" ")
    bits = [int(x) for x in bits.split(",")]
    queries.append(bits)

for bits in queries:
    fpl = len(bits)*tcut
    fpu = len(bits)/tcut
    print 'fpcount bounds: %f and %f' % (fpl, fpu)

    res = coll.aggregate([
        { "$match" : {"fpcount":{"$gt": fpl, "$lte":fpu}}},
        { "$unwind" : "$fp"},
        { "$match" : { "fp" : { "$in":bits}}},
        { "$group" : {"_id":"$molregno", 
                      "molregno":{"$first":"$molregno"},
                      "fpmatches":{"$sum":1}, 
                      "totalcount" : { "$first" : "$fpcount"},
                      "smi" : { "$first" : "$smi"}
                      }
        },
        { "$project": {"_id" : 1, 
                       "molregno":1,
                       "tanimoto":{ "$divide" : [ "$fpmatches" , { "$subtract" : [ { "$add" : [ len(bits) , "$totalcount"]} , "$fpmatches"] } ] } ,
                       "smi" : 1
                       }
        },
        { "$match" : {"tanimoto":{"$gte":tcut}}},
        { "$sort" : {"tanimoto":1}}
        ])

## pull profiling info
db = client.sim
coll = db.system.profile
times = [x['millis'] for x in  coll.find().limit(nmol).sort( "ts", pymongo.DESCENDING )]
o = open('times.txt', 'w')
for l, t in zip([len(x) for x in queries], times):
    o.write("%d,%d\n" % (l,t))
o.close()

