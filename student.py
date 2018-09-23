import pandas

def load_students(path):
	df = pandas.read_csv(path, dtype = str)
	students = df.apply(Student, axis = 1)
	return students

class Student:
	def __init__(self, df_row):
		for key, value in df_row.items():
			self.__dict__[key] = value