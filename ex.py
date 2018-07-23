cond = input("Wprowadz wartosc warunku: ")

class MyException(Exception):

	def __init__(self, p):
		super(MyException, self).__init__("Exception! {} is more than 10".format(p))

def method(parameter, condition):

	if parameter > condition:
		raise MyException(parameter)
	else:
		print("No errors")

while True:
	value = input("Please enter value to equal or 0 to quit: ")
	if value == 0:
		break
	try:
		method(value, cond)
	except MyException as ex:
		print(ex)
