import pymongo, sys
client = pymongo.MongoClient()
db = client.sim
coll = db.compounds

x = open('fp.txt', 'r')
x.readline()
n = 0

docs = []
for line in x:
    n += 1
    #    sys.stdout.write( '\r%d' % n)
    #sys.stdout.flush()

    if line.strip().find(" ") == -1: continue
    molregno, bits = line.strip().split(" ")
    bits = [int(x) for x in bits.split(",")]

    doc = {"molregno":molregno,
           "fp":bits,
           "fpcount":len(bits),
           "smi":""}
    docs.append(doc)
    if n % 2000 == 0:
        coll.insert(docs)
        sys.stdout.write('\rWrote %d' % (n))
        sys.stdout.flush()
        docs = []

