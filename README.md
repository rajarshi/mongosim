This repository accompanies a [post](http://blog.rguha.net/?p=1300) where I describe the fingerprint based similarity searches in MongoDB. The post and code was inspired by a [Datablend post](http://datablend.be/?p=265) who described this approach and my code is pretty much what they described (just packaged in a Python wrapper).

To load the fingerprints and then run the benchmark unzip ```fp.txt.zip``` and then run the scripts:
```
unzip fp.txt.zip
python fpload.py
python profile.py
```
On completion, the time for each query along with the bit length of the query structure will be in ```times.txt```. This assumes you have a MongoDB instance running on the local machine at the default port
