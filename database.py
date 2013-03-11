#! /usr/bin/python

import sqlite3

class PhotontisticsDatabase():
	db_file_name = 'photontistics.sqlite3'
	db_conn = ''

	def __init__(self):
		self.db_conn = sqlite3.connect(self.db_file_name)
		self.db_conn.row_factory = sqlite3.Row

	def __del__(self):
		self.db_conn.close()


	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d


	def initDB(self):
		c = self.db_conn.cursor()
		try:
			c.execute('''CREATE TABLE "photo" (
					"id" INTEGER PRIMARY KEY  NOT NULL , 
					"sha1" VARCHAR(32) NOT NULL  DEFAULT 0, 
					"filename" TEXT NOT NULL  DEFAULT "", 
					"iso" FLOAT, 
					"exposure" FLOAT, 
					"fnumber" FLOAT, 
					"lens_model" TEXT, 
					"lens_maker" TEXT, 
					"focal_length" INTEGER, 
					"flash" BOOL)''')
			print 'PhotontisticsDatabase::created'

		except Exception, e:
			print e


	def loadPhoto(self, photo):
		c = self.db_conn.cursor()
		c.execute("SELECT * FROM photo WHERE filename=?", [photo.filename])

		return c.fetchone()



	def addPhoto(self, photo):
		if self.loadPhoto(photo):
			return

		attributes = {"filename": photo.filename,
				"iso":            photo.iso,
				"exposure":       photo.exposure,
				"fnumber":        photo.fnumber,
				"lens_model":     photo.lens_model,
				"lens_maker":     photo.lens_maker,
				"focal_length":   photo.focal_length,
				"flash":          photo.flash,
				}

		c = self.db_conn.cursor()
		c.execute(''' INSERT INTO "main"."photo" (
				"filename",
				"iso",
				"exposure",
				"fnumber",
				"lens_model",
				"lens_maker",
				"focal_length",
				"flash") 
				VALUES (:filename, :iso, :exposure,
				:fnumber, :lens_model, :lens_maker, 
				:focal_length, :flash)''', attributes)
		self.db_conn.commit()

		return c.lastrowid

	def updatePhoto(self, photo):
		attributes = {"id": photo.photo_id,
				"filename": photo.filename,
				"iso":            photo.iso,
				"exposure":       photo.exposure,
				"fnumber":        photo.fnumber,
				"lens_model":     photo.lens_model,
				"lens_maker":     photo.lens_maker,
				"focal_length":   photo.focal_length,
				"flash":          photo.flash,
				}

		c = self.db_conn.cursor()
		c.execute('''UPDATE "main"."photo" SET  
				"filename" = :filename, 
				"iso" = :iso, 
				"exposure" = :exposure, 
				"fnumber" = :fnumber, 
				"lens_model" = :lens_model, 
				"lens_maker" = :lens_maker, 
				"focal_length" = :focal_length, 
				"flash" = :flash 
				WHERE  "id" = :id''', attributes)
		self.db_conn.commit()



	def getAllPhotos(self):
		c = self.db_conn.cursor()
		c.execute("SELECT * FROM photo")

		return c.fetchall()



