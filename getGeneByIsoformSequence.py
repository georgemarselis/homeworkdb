#!/opt/local/bin/python3.4

import pymysql
import getopt
import sys

def usage( ):
	helpString = """
Script8. getGeneByIsoformSequence.py –s "ακολουθία"
	Τυπώνει στην οθόνη του χρήστη το όνομα του γονιδίου και το όνομα της
	αντίστοιχης πρωτεΐνης για την οποία υπάρχει κάποια ισομορφή που περιέχει
	την ακολουθία X (όπου Χ η ακολουθία που δίνεται ως όρισμα)."""

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
		elif o in ("-p", "--sequence"):
			sequence = a
		else:
			assert False, "unhandled option"

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

	selectQuery = "select protein.geneId, protein.proteinName from isomorph inner join protein on isomorph.proteinId = protein.proteinId where isomorph.isomorphFASTASequence like '%%%s%%';" % sequence
	cursor.execute( selectQuery )


	#substitute for fetchone
	for row in cursor:
		print( row )

	cursor.close( )

if __name__ == "__main__":
	main()