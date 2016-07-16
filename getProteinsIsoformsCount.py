#!/opt/local/bin/python3.4

import pymysql


host       = '192.168.1.4';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "pez2015_project2501a"

# # connect to db
conn = pymysql.connect( host, user, password )
if conn != -1 :
	print( 'database connection established' )
else:
	print( 'Houston we have a problem' )

conn.begin( )
cursor = conn.cursor( )
#turn this into a stored procedure

cursor.execute( "use " + db )
conn.commit( )

selectQuery = "select isomorph.proteinid, count( isomorph.isomorphFASTASequence ) from isomorph group by proteinId;"
cursor.execute( selectQuery )

#substitute for fetchone
for row in cursor:
	print( row )

cursor.close( )#!/opt/local/bin/python3.4

import pymysql
import getopt
import sys

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs:v", ["help", "output="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print( err ) # will print something like "option -a not recognized"
		usage( )
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
		    verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-o", "--output"):
			output = a
		else:
			assert False, "unhandled option"

	host       = '192.168.1.4';
	user       = 'root';
	password   = '12345'
	defaultcharset    = 'utf8'
	defaultcollation  = 'utf8_general_ci'


	db = "pez2015_project2501a"

	optlist, args = getopt.getopt(args, 's:')

	# # connect to db
	conn = pymysql.connect( host, user, password )
	if conn != -1 :
		print( 'database connection established' )
	else:
		print( 'Houston we have a problem' )

	conn.begin( )
	cursor = conn.cursor( )
	#turn this into a stored procedure

	cursor.execute( "use " + db )
	conn.commit( )

	selectQuery = "select isomorph.proteinid, count( isomorph.isomorphFASTASequence ) from isomorph group by proteinId;"
	cursor.execute( selectQuery )

	#substitute for fetchone
	for row in cursor:
		print( row )

	cursor.close( )

if __name__ == "__main__":
	main()
