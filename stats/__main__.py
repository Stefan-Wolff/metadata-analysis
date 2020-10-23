#!/usr/bin/env python
#

import os
import logging
import sys
import json



DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/ieee_filtered.json')



def run():
	if 2 > len(sys.argv):
		raise Exception("Analysis to run not given!") 

	stats_id = sys.argv[1]

	logging.basicConfig(format		=	"%(asctime)s %(levelname)s: %(message)s", 
						filename	=	os.path.join(os.path.dirname(__file__), '../logs/stats_' + stats_id + '.log'),
						level		=	logging.INFO)
	logging.getLogger().addHandler(logging.StreamHandler())


	logging.info("start analysis " + stats_id + " ..")
	

	with open(DATA_PATH) as file:
		data = json.load(file)
	
	script = "stat_" + stats_id
	exec("import " + script)
	exec("global count; global num; count,num = " + script + ".run(data)")

	if count != -1:
		percent = round(100 * count / num, 4)
		logging.info("analysis " + stats_id + ": " + str(percent) + " % (" + str(count) + " / " + str(num) + ")")

	
if "__main__" == __name__:
	try:
		run()
	except:
		logging.exception(sys.exc_info()[0])