import os
import sqlite3 as lite
import csv
import re


def main():
	con = lite.connect('cs1656.sqlite')

	with con:
		cur = con.cursor()

		########################################################################
		### CREATE TABLES ######################################################
		########################################################################
		# DO NOT MODIFY - START
		cur.execute('DROP TABLE IF EXISTS Actors')
		cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

		cur.execute('DROP TABLE IF EXISTS Movies')
		cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

		cur.execute('DROP TABLE IF EXISTS Directors')
		cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

		cur.execute('DROP TABLE IF EXISTS Cast')
		cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

		cur.execute('DROP TABLE IF EXISTS Movie_Director')
		cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
		# DO NOT MODIFY - END

		########################################################################
		### READ DATA FROM FILES ###############################################
		########################################################################
		# actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
		# UPDATE THIS

		file_in = ['actors.csv', 'cast.csv', 'directors.csv', 'movie_dir.csv', 'movies.csv']

		for f in file_in:
			# make sure file exists
			if os.path.isfile(os.path.join(os.getcwd(), f)):
				# open csv, set dilimter to new line, read and print line by line
				with open(f, 'r') as csvfile:
					reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
					for row in reader:
						r = ','.join(row).split(',')
						if f == 'actors.csv':
							for i in range(1, 4):
								# add quotes to strings
								r[i] = "'" + r[i] + "'"
							r = ','.join(r)
							print(r)
							cur.execute("INSERT INTO Actors VALUES(" + r + ")")
						elif f == 'cast.csv':
							r[2] = "'" + r[2] + "'"
							r = ','.join(r)
							print(r)
							cur.execute("INSERT INTO Cast VALUES(" + r + ")")
						if f == 'directors.csv':
							for i in range(1, 3):
								# add quotes to strings
								r[i] = "'" + r[i] + "'"
							r = ','.join(r)
							print(r)
							cur.execute("INSERT INTO Directors VALUES(" + r + ")")
						elif f == 'movie_dir.csv':
							r = ','.join(r)
							print(r)
							cur.execute("INSERT INTO Movie_Director VALUES(" + r + ")")
						elif f == 'movies.csv':
							r[1] = "'" + r[1] + "'"
							r = ','.join(r)
							print(r)
							cur.execute("INSERT INTO Movies VALUES(" + r + ")")
		con.commit()


		########################################################################
		### QUERY SECTION ######################################################
		########################################################################
		queries = {}

		# DO NOT MODIFY - START
		# DEBUG: all_movies ########################
		queries['all_movies'] = '''
	SELECT * FROM Movies
	'''
		# DEBUG: all_actors ########################
		queries['all_actors'] = '''
	SELECT * FROM Actors
	'''
		# DEBUG: all_cast ########################
		queries['all_cast'] = '''
	SELECT * FROM Cast
	'''
		# DEBUG: all_directors ########################
		queries['all_directors'] = '''
	SELECT * FROM Directors
	'''
		# DEBUG: all_movie_dir ########################
		queries['all_movie_dir'] = '''
	SELECT * FROM Movie_Director
	'''
		# DO NOT MODIFY - END
	#
	# 	########################################################################
	# 	### INSERT YOUR QUERIES HERE ###########################################
	# 	########################################################################
	# 	# NOTE: You are allowed to also include other queries here (e.g.,
	# 	# for creating views), that will be executed in alphabetical order.
	# 	# We will grade your program based on the output files q01.csv,
	# 	# q02.csv, ..., q12.csv
	#
	# 	# Q01 ########################
	# 	queries['q01'] = '''
	# '''
	#
	# 	# Q02 ########################
	# 	queries['q02'] = '''
	# '''
	#
	# 	# Q03 ########################
	# 	queries['q03'] = '''
	# '''
	#
	# 	# Q04 ########################
	# 	queries['q04'] = '''
	# '''
	#
	# 	# Q05 ########################
	# 	queries['q05'] = '''
	# '''
	#
	# 	# Q06 ########################
	# 	queries['q06'] = '''
	# '''
	#
	# 	# Q07 ########################
	# 	queries['q07'] = '''
	# '''
	#
	# 	# Q08 ########################
	# 	queries['q08'] = '''
	# '''
	#
	# 	# Q09 ########################
	# 	queries['q09'] = '''
	# '''
	#
	# 	# Q10 ########################
	# 	queries['q10'] = '''
	# '''
	#
	# 	# Q11 ########################
	# 	queries['q11'] = '''
	# '''
	#
	# 	# Q12 ########################
	# 	queries['q12'] = '''
	# '''
	#
	#
	# 	########################################################################
	# 	### SAVE RESULTS TO FILES ##############################################
	# 	########################################################################
	# 	# DO NOT MODIFY - START
		for (qkey, qstring) in sorted(queries.items()):
			try:
				cur.execute(qstring)
				all_rows = cur.fetchall()

				print ("=========== ",qkey," QUERY ======================")
				print (qstring)
				print ("----------- ",qkey," RESULTS --------------------")
				for row in all_rows:
					print (row)
				print (" ")

				save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
				if (save_to_file):
					with open(qkey+'.csv', 'w') as f:
						writer = csv.writer(f)
						writer.writerows(all_rows)
						f.close()
					print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")

			except lite.Error as e:
				print ("An error occurred:", e.args[0])
	# 	# DO NOT MODIFY - END


if __name__ == "__main__":
	main()
