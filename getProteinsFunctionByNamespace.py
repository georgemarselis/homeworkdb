#!/opt/local/bin/python3.4

import pymysql
import getopt
import sys
import os

def usage( ):
	helpString = """
getProteinsFunctionByNamespace.py –n "κατηγορία λειτουργίας"
	Τυπώνει στην οθόνη του χρήστη τον όρο και το όνομα των λειτουργιών που
	σχετίζονται με πρωτεΐνες που ο κωδικός πρωτεΐνης τους ξεκινάει από "P"
	και η λειτουργία ανήκει στην κατηγορία Χ (όπου Χ η κατηγορία λειτουργίας
	που δίνεται ως όρισμα).

"""

	print( helpString )

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hn:v", ["help", "namespace="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print( err ) # will print something like "option -a not recognized"
		usage( )
		sys.exit(2)
	namespace = None
	verbose = False
	for o, a in opts:
		if o == "-v":
		    verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-n", "--namespace"):
			namespace = a
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

	selectQuery = "select geneOntology.proteinId, geneOntology.biological_process from geneOntology where ontologyFunction like '%%%s%%' and geneOntology.proteinid like 'P%%';" % namespace
	cursor.execute( selectQuery )


	#substitute for fetchone
	for row in cursor:
		print( row )

	cursor.close( )

if __name__ == "__main__":
	main()
