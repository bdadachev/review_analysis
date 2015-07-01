import subprocess
from secrets import mongo

# dump the database to ./mongo.LOCAL_DB
subprocess.call([
	"mongodump",
	"-h", "{}:{}".format(mongo.LOCAL_HOST, mongo.LOCAL_PORT),
	"-d", mongo.LOCAL_DB,
	"-o", "."
])

# and upload to HEROKU
subprocess.call([
	"mongorestore", 
	"-h", "{}:{}".format(mongo.HEROKU_HOST, mongo.HEROKU_PORT),
	"-d", mongo.HEROKU_DB,
	"-u", mongo.HEROKU_USER,
	"-p", mongo.HEROKU_PWD,
	"./{}".format(mongo.LOCAL_DB)
])
