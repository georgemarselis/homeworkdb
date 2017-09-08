#!/opt/local/bin/python3.4

import sys
import urllib.request
import json
import multiprocessing
import http.client 
from clint.textui import colored


def callHintkb( protein ):
	hintkbURL = "http://hintkb.ceid.upatras.gr/api/functions/byprotein/"
	URL = hintkbURL + protein
	response = urllib.request.urlopen( "http://google.com	" )
	try:
		response = urllib.request.urlopen( URL )
	except:
		print( colored.red(  "Failed: " + URL ) ) 
	else:
		print( colored.green(  "\t" + URL ) )

	restResult = response.read( ) 
	# {"function_id":17269,"go_term":"0033603","function_name":"positive regulation of dopamine secretion","function_namespace":"biological_process"}
	result = restResult.decode( 'UTF-8' ) 
	return result
	



if __name__ == '__main__':

	result = { }
	proteins  = [ "X2KUB5", "X2KUK3", "X2KUK8", "X2KUL2", "X2KUL5", "X2L0E3", 
				  "X2L0F3", "X2L0F7", "X2L0G2", "X2LA36", "X2LA51", "X2LAP7", 
				  "X2LAR2", "X2LAR8", "X2LAS0", "X2LAS7", "X2LAS9", "X2LI34", 
				  "X2LI64", "X4Y8Z9", "X5DNX0", "X5DR79"
				]

	with multiprocessing.Pool(100) as p:
		result = p.map( callHintkb, proteins)
	
	print( colored.cyan( "\n".join( result) + "\n############################\n" ) )