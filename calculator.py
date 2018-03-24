#!/usr/bin/env python3

import getopt, sys, configparser
from datetime import datetime, date
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
			self._usage()
		
	def _usage(self):
		for item in self._opts:
			if (item[0] == '-h') | (item[0] == '--help'):
				print("Usage: calculator.py -C cityname -c configfile -d userdata -o resltdata")
				break;

class Config:
	def __init__(self, configname, cityname):
		self._config = configparser.ConfigParser()
		self._config.read(configname)
		self.cityname = cityname
		self.jishul, self.jishuh, self.total_rate = self.get_value()

	def get_value(self):
		total_rate = 0
		try:
			jishul = float(self._config[self.cityname]['JiShuL'])
			jishuh = float(self._config[self.cityname]['JiShuH'])
			for index in self._config[self.cityname]:
				if (index != 'jishul') & (index != 'jishuh'):
					total_rate += float(self._config[self.cityname][index])
				else:
					continue
		except:
			print("Parameter Error")
		return jishul, jishuh, total_rate

class Userdata():
	def __init__(self, userfile):
		self.file = userfile

	def get_data(self):
		data_list = []
		with open(self.file) as file:
			for line in file:
				employee_id, salary = line.split(',')
				try:
					data_list.append((int(employee_id.strip()), int(salary.strip())))
				except:
					print("Parameter Value")
		return data_list

 
class Calculator():

	def __init__(self, config):
		self.config = config
		self._threshold = 3500
		self._tax_table = [
				(80000, 0.45, 13505),
				(55000, 0.35, 5505),
				(35000, 0.3, 2755),
				(9000, 0.25, 1005),
				(4500, 0.2, 555),
				(1500, 0.1, 105),
				(0, 0.03, 0)
	
			]
		super().__init__()

	def calculate(self, user_data):
		employee_id, salary = user_data

		if salary < self.config.jishul:
			insurance = self.config.jishul * self.config.total_rate	
		elif salary > self.config.jishuh:
			insurance = self.config.jishuh * self.config.total_rate
		else:
			insurance = salary * self.config.total_rate

		request = salary - insurance - self._threshold

		if request < 0:
			tax = 0
		else:
			for item in self._tax_table:
				if request > item[0]:
					tax = request * item[1] - item[2]
					break

		left_salary = salary - insurance - tax

		return employee_id, salary, format(insurance, '.2f'), \
			format(tax, '.2f'), format(left_salary, '.2f')

class Execute:
	def __init__(self):
		try:
			self.args = Args()
			config_path = self.args.get_filename('-c')
			city_name = self.args.get_filename('-C')
			if city_name == None:
				city_name == 'DEFAULT'
			self.config = Config(config_path, city_name)
			self.calculator = Calculator(self.config)
			self.user = Userdata(self.args.get_filename('-d'))
		except:
			self.args._usage()
		finally:
			self.ouput = self.args.get_filename('-o')
	def run(self):
		t = datetime.now()
		time_str = datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
		with open(self.output, 'w') as file:
			for item in self.user.get_data():
				output = self.calculator.calculate(item)
				line = '{},{},{},{},{},{}\n'.format(output[0], output[1], \
				output[2], output[3], output[4], time_str)
				file.write(line)

if __name__ == '__main__':
	execute = Execute()
	execute.run()
	
