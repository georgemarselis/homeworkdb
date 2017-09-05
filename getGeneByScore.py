#!/opt/local/bin/python3.4

import pymysql
import getopt
import sys
import os

def usage( ):
	helpString = """
Τυπώνει στην οθόνη του χρήστη το όνομα, το σύμβολο και το σκορ σχετικότητας 
με την ασθένεια για τα γονίδια που το σκορ συσχέτισης με την ασθένεια είναι 
μεγαλύτερο του Χ (όπου Χ το σκορ που δίνεται ως όρισμα) σε κατάταξη σύμφωνα
με το σκορ (το μεγαλύτερο σκορ πρώτο)
"""
	print( helpString )

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs:v", ["help", "score="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print( err ) # will print something like "option -a not recognized"
		sys.exit(2)
	score = "0.01"
	verbose = False
	for o, a in opts:
		if o == "-v":
		    verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-s", "--score"):
			score = a
		else:
			assert False, "unhandled option"

	host       = '192.168.1.5';
	user       = 'root';
	password   = '12345'
	defaultcharset    = 'utf8'
	defaultcollation  = 'utf8_general_ci'

	db = "project2501a_pez"

	if "PEZ_HOST" in os.environ:
		host = str(os.environ['PEZ_HOST'])
	if "PEZ_DATABASE" in os.environ:
		db = str(os.environ['PEZ_DATABASE'])
	if "PEZ_USER" in os.environ:
		user = str(os.environ['PEZ_USER'])
	if "PEZ_PASSWORD" in os.environ:
		password = str(os.environ['PEZ_PASSWORD'])


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
	
	selectQuery = "select gene.geneName, gene.geneId, gene.disgenetScore from gene where disgenetscore > %s order by disgenetscore desc"
	cursor.execute( selectQuery, (score, ) )

	#substitute for fetchone
	for row in cursor:
		print( row )

	cursor.close( )

if __name__ == "__main__":
	main()
