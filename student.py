import pandas

def load_students(path):
	df = pandas.read_csv(path, dtype = str)
	students = df.apply(Student, axis = 1)
	return students

class Student:
	def __init__(self, df_row):
		self.email = df_row["email"]
		self.username = df_row["username"]
		self.password = df_row["password"]
		self.name = df_row["name"]
		self.sid = df_row["sid"]