# s3upload
Watches a directory and uploads new files to specified s3 bucket

### Running the server
To run the server, run:

```
python3 watch_for_changes.py config.ini 
```

### Configuration

Warning: All the parameters are required. Sample below

```
[Configuration]
# Directory to watch
input: /root/lpTest/test
# Ignore Files with extenstions (semicolon separated)
extensions: *.log;*.py;*.ini;*.swp;*.swx
# tls usually set to True
tls : True
# S3 Endpoint 
endpoint: s3-eu-west-1.amazonaws.com
# S3 Access Key
access_key: xxxxxxx
# S3 Security Key
security_key: xxxxxxxxx
# S3 Bucket name
bucket_name: xxxxxxx
# Results from the upload are logged to this file
logFile : ./results.log 
```
### Log Format

```
<filename> <response code> <epoch timestamp>
```

### Limitations

* only files dumped to the input dir are uploaded (no directories inside folder yet!)
* no failure recovery and retries (upload fails, network fail etc.,) only logs 
* no delete feature (only uploads new files) 
* multiple files can’t be dumped at once (e.g 10000 files, susceptible to failures due to resource limit)
* there should be no errors in config file 

### TODO

* Delete and Modify files
* More threaded support with Thread pools

### Resource

* http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html
