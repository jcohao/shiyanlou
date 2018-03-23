#!/usr/bin/env python3

import getopt, sys, configparser

class Args:
	def __init__(self):	
		self._opts, self._args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help"])

	def get_filename(self, index):
		try:
			value = None
			for item in self._opts:
				if index == item[0]:
					value = item[1]
			return value
		except (ValueError, IndexError):
			print("Parameter Error")

class Config:
	def __init__(self, configname):
		self._config = configparser.ConfigParser()
		self._config.read(configname)

	def get_value(self, cityname):
		total_rate = 0
		jishul = float(self._config[cityname]['JiShuL'])
		jishuh = float(self._config[cityname]['JiShuH'])
		for index in self._config[cityname]:
			if (index != 'jishul') & (index != 'jishuh'):
				total_rate += float(self._config[cityname][index])
			else:
				continue
		return jishul, jishuh, total_rate

if __name__ == '__main__':
	args = Args()
		if index in ('-h', '--help'):
			print("help")
			sys.exit() 
#	config_path = args.get_filename('-c')
#	city_name = args.get_filename('-C')
#	if city_name == None:
#		city_name = 'DEFAULT'
#	config = Config(config_path)
	
	
