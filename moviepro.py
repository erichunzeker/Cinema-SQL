import os
import sqlite3 as lite
import csv
import re


def main():
	con = lite.connect('cs1656.sqlite')

	with con:
		cur = con.cursor()

		# CREATE TABLES
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

		# READ DATA FROM FILES
		# actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv

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

		# QUERY SECTION

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
	# 	INSERT YOUR QUERIES HERE

	# TODO:
		# query 3
		# query 6 - add ties
		# query 7
		# query 8
		# query 10
		# query 12

	# Q01
		queries['q01'] = '''
			SELECT fname, lname 
			FROM Actors
			WHERE aid in (SELECT aid FROM Movies as M1 INNER JOIN Cast as C1 on M1.mid = C1.mid where M1.year >= 1980 and M1.year <= 1990 
					INTERSECT 
			SELECT aid FROM Movies as M2 INNER JOIN Cast as C2 on M2.mid = C2.mid where M2.year >= 2000); 
		'''

	# Q02
		queries['q02'] = '''
			SELECT title, year
			FROM Movies
			WHERE year = (SELECT year FROM Movies as M WHERE M.title = 'Rogue One: A Star Wars Story') and rank > 
				(SELECT rank FROM Movies as M WHERE M.title = 'Rogue One: A Star Wars Story')
			ORDER BY title ASC;
		'''






	# Q03 - List all the actors (first and last name) who played in a Star Wars movie (i.e., title like '%Star Wars%')
		# in decreasing order of how many Star Wars movies they appeared in. If an actor plays multiple roles in the
		# same movie, count that still as one movie. If there is a tie, use the actor's last and first name to
		# generate a full sorted order.
		queries['q03'] = '''
	SELECT fname, lname
	FROM Actors as A
	WHERE aid in (SELECT aid, count(aid) as C FROM Movies as M INNER JOIN Cast as C on M.mid = C.mid WHERE M.title LIKE '%Star Wars%');
	'''







	# Q04
		queries['q04'] = '''
			SELECT fname, lname
			FROM Actors as A
			INNER JOIN Cast as C on A.aid = C.aid
			WHERE C.mid IN (
				SELECT mid 
				FROM Movies
				WHERE year < 1985)
			ORDER BY A.lname, A.fname ASC;
		'''

	# Q05
		queries['q05'] = '''
			SELECT fname, lname, count(M.did)
			FROM Movie_Director as M 
			INNER JOIN Directors as D on M.did = D.did
			GROUP BY M.did
			ORDER BY count(M.did) DESC 
			LIMIT 20;
		'''








	# Q06 - Find the top 10 movies with the largest cast (title, number of cast members) in decreasing order. Note:
		# show all movies in case of a tie.
		# todo: add ties
	# 	queries['q06'] = '''
	# # SELECT title, count(title)
	# # FROM Movies as M
	# # INNER JOIN Cast as C on M.mid = C.mid
	# # GROUP BY title
	# # ORDER BY count(title) DESC
	# # LIMIT 10;
	# '''
		queries['a1'] = '''
	CREATE VIEW frequencies as
	select m.title, count(aid) as cast_cnt
	from Movies m, Cast c
	where m.mid = c.mid
	group by m.title;
	'''
		queries['q06'] = '''
	SELECT *
	FROM frequencies
	ORDER BY cast_cnt DESC;
		'''
		# WHERE cast_cnt = (select max(cast_cnt) from frequencies)








	# Q07 - Find the movie(s) whose cast has more actresses than actors (i.e., gender=female vs gender=male). Show the
		# title, the number of actresses, and the number of actors in the results. Sort alphabetically,
		# by movie title.
		queries['b2'] = '''
	CREATE VIEW female_cast_cnt as
	SELECT m.title, m.mid, count(*) as female_cnt
	FROM Actors a, Cast c, Movies m 
	WHERE m.mid = c.mid AND c.aid = a.aid AND a.gender = 'Female'
	GROUP BY m.mid;
	'''
		queries['b21'] = '''
	CREATE VIEW male_cast_cnt as
	SELECT m.mid, count(*) as male_cnt
	FROM Actors a, Cast c, Movies m 
	WHERE m.mid = c.mid AND c.aid = a.aid AND a.gender = 'Male'
	GROUP BY m.mid;
	'''
		queries['q07'] = '''
	SELECT f.title, f.female_cnt, m.male_cnt
	FROM female_cast_cnt f LEFT OUTER JOIN 
	male_cast_cnt m ON f.mid = m.mid
	WHERE f.female_cnt > m.male_cnt OR m.male_cnt ISNULL 
	GROUP BY f.mid;
	'''








	# Q08 - Find all the actors who have worked with at least 7 different directors. Do not consider cases of
		# self-directing (i.e., when the director is also an actor in a movie), but count all directors in a movie
		# towards the threshold of 7 directors. Show the actor's first, last name, and the number of directors he/she
		# has worked with. Sort in decreasing order of number of directors.
		queries['q08'] = '''
	'''








	# Q09
		queries['aa1'] = '''
			CREATE VIEW qualifying AS
			SELECT a.aid, min(m.year) as yc
			FROM Movies m, Actors a, Cast c
			WHERE m.mid = c.mid AND a.aid = c.aid AND c.aid IN (
				SELECT a1.aid 
				FROM Actors	a1
				WHERE lower(a1.fname) LIKE 'T%'
			)
			GROUP BY a.aid;
		'''
		queries['q09'] = '''
			SELECT a.fname, a.lname, count(q.aid)
			FROM qualifying q, Actors a, Cast c, Movies m
			WHERE q.aid = a.aid AND q.yc = m.year AND c.mid = m.mid AND c.aid = q.aid
			GROUP BY q.aid
			ORDER BY count(q.aid) desc 
		'''




	# Q10 - Find instances of nepotism between actors and directors, i.e., an actor in a movie and the director having
		# the same last name, but a different first name. Show the last name and the title of the movie,
		# sorted alphabetically by last name.
		queries['q10'] = '''
	'''




	# Q11 - The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the
		# "co-acting" graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him
		# have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon
		# number 2, etc. List all actors whose Bacon number is 2 (first name, last name). You can familiarize yourself
		#  with the concept, by visiting The Oracle of Bacon.

		queries['a2'] = '''
			create view bacon1 as
			SELECT DISTINCT c1.aid 
			FROM Cast c1
			WHERE c1.mid in (
				SELECT c.mid
				FROM Cast c
				WHERE c.aid = (SELECT a.aid 
								FROM Actors a
								WHERE a.lname = 'Bacon')
			);
		'''
		queries['a3'] = '''
			create view bacon2 as
			SELECT DISTINCT c1.aid 
			FROM Cast c1
			WHERE c1.mid in (
				SELECT c.mid
				FROM Cast c
				WHERE c.aid in (SELECT * FROM bacon1)
			);
		'''
		queries['q11'] = '''
			SELECT a1.fname, a1.lname
			FROM bacon2 b, Actors a1
			WHERE b.aid = a1.aid AND b.aid NOT IN (SELECT aid from Actors a WHERE a.lname = 'Bacon');
		'''






	# Q12 - Assume that the popularity of an actor is reflected by the average rank of all the movies he/she has acted
		# in. Find the top 20 most popular actors (in descreasing order of popularity) -- list the actor's first/last
		# name, the total number of movies he/she has acted, and his/her popularity score. For simplicity,
		# feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).
		queries['q12'] = '''
		
	'''






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
