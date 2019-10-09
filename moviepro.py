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
	# Q03
		queries['q03'] = '''
			SELECT a.aid, a.fname, a.lname, count(DISTINCT c.mid) as mv_cnt
			FROM Movies m, Cast c, Actors a
			WHERE m.mid = c.mid AND a.aid = c.aid AND m.title LIKE "%Star Wars%"
			GROUP BY a.aid
			ORDER BY mv_cnt DESC, a.lname ASC, a.fname ASC;
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
	# Q06
		queries['d1'] = '''
			CREATE VIEW cnt_limited as
			select count(aid) as cast_cnt
			from Movies m, Cast c
			where m.mid = c.mid
			group by m.mid
			order by cast_cnt DESC
			LIMIT 10;
		'''

		queries['d3'] = '''
					CREATE VIEW lowest as
					select min(cast_cnt) as lowest
					from cnt_limited;
				'''

		queries['d2'] = '''
					CREATE VIEW cnt_all as
					select m.title as title, count(aid) as cast_cnt
					from Movies m, Cast c
					where m.mid = c.mid 
					group by m.mid
					order by cast_cnt DESC;
				'''

		queries['q06'] = '''
			select a.title, a.cast_cnt
			from cnt_all a, lowest low
			WHERE a.cast_cnt >= low.lowest
		'''
	# Q07
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
			FROM female_cast_cnt f 
			LEFT OUTER JOIN male_cast_cnt m 
			ON f.mid = m.mid
			WHERE f.female_cnt > m.male_cnt OR m.male_cnt ISNULL 
			GROUP BY f.mid
			ORDER BY f.title ASC;
		'''
	# Q08
		queries['b1'] = '''
			CREATE VIEW dir_cnt as
			SELECT a.aid, a.fname, a.lname, count(DISTINCT md.did) as co_cnt
			FROM Movies m, Actors a, Cast c, Movie_Director md, Directors d
			WHERE m.mid = c.mid AND m.mid = md.mid AND md.did = d.did AND c.aid = a.aid 
			GROUP BY a.aid;
		'''

		queries['q08'] = '''
			SELECT * 
			FROM dir_cnt
			WHERE co_cnt > 6
			ORDER BY co_cnt DESC;
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

	# Q10
		queries['q10'] = '''
			SELECT d.lname, m.title 
			FROM Cast c, Movies m, Directors d, Actors a, Movie_Director md
			WHERE md.mid = m.mid AND c.mid = md.mid AND d.did = md.did AND a.aid = c.aid AND d.lname = a.lname AND d.fname != a.fname
			ORDER BY d.lname ASC;
		'''

	# Q11
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

	# Q12
		queries['q12'] = '''
			SELECT a.aid, a.fname, a.lname, count(c.mid), AVG(m.rank)
			FROM Movies m, Actors a, Cast c
			WHERE m.mid = c.mid AND a.aid = c.aid 
			GROUP BY a.aid
			ORDER BY AVG(m.rank) DESC
			LIMIT 20;
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
