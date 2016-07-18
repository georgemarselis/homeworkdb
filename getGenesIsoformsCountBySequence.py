#!/opt/local/bin/python3.4

import pymysql
import getopt
import sys
import os

def usage( ):
	helpString = """
Script 10. 	.py –s «ακολουθία»
	Τυπώνει στην οθόνη του χρήστη το σύμβολο του γονιδίου και το πλήθος των
	ισομορφών της αντίστοιχης πρωτεΐνης που περιέχουν την ακολουθία X (όπου
	Χ η ακολουθία που δίνεται ως όρισμα).
"""

	print( helpString )

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs:v", ["help", "sequence="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print( err ) # will print something like "option -a not recognized"
		usage( )
		sys.exit(2)
	sequence = None
	verbose = False
	for o, a in opts:
		if o == "-v":
		    verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-s", "--sequence"):
			sequence = a
		else:
			assert False, "unhandled option"

	host       = '192.168.1.4';
	user       = 'root';
	password   = '12345'
	defaultcharset    = 'utf8'
	defaultcollation  = 'utf8_general_ci'

	db = "project2501a_pez"

	if str(os.environ['PEZ_HOST']):
		host = str(os.environ['PEZ_HOST'])
	if str(os.environ['PEZ_USER']):
		user = str(os.environ['PEZ_USER'])
	if str(os.environ['PEZ_PASSWORD']):
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

	selectQuery = "select protein.geneId, foo.count from ( select count(isomorph.proteinId) as count, isomorph.proteinId from isomorph where isomorph.isomorphFASTASequence like '%%%s%%' group by isomorph.proteinId ) as foo inner join protein on foo.proteinId = protein.proteinId ;" % sequence
	cursor.execute( selectQuery )


	#substitute for fetchone
	for row in cursor:
		print( row )

	cursor.close( )

if __name__ == "__main__":
	main()
