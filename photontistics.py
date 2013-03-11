#! /usr/bin/python

import os
import sys
import shelve
import hashlib
import fnmatch

from PIL import Image
from PIL.ExifTags import TAGS

from database import PhotontisticsDatabase

PICTURE_EXTENSIONS = ''
DB = PhotontisticsDatabase()



class Photo():
	sha1 = ''
	photo_id = ''
	filename = ''
	iso = ''
	exposure = ''
	fnumber = ''
	lens_model = ''
	lens_maker = ''
	focal_length = ''
	flash = ''

	def __init__(self, data=None):
		self.full_path_and_name = ''
		self.sha1 = ''

		if not data == None:
			self.photo_id = data['id']
			self.filename = data['filename']
			self.iso = data['iso']
			self.exposure = data['exposure']
			self.fnumber = data['fnumber']
			self.lens_model = data['lens_model']
			self.lens_maker = data['lens_maker']
			self.focal_length = data['focal_length']
			self.flash = data['flash']


	def loadExifData(self):
		print 'loadExifData'

	def setFileName(self, local_filename):
		print 'Photo::setFileName to ' + local_filename
		self.filename = local_filename
		# fp = open(self.filename, 'r')
		# self.sha1 = hashlib.sha1(fp.read()).hexdigest()

	def procExifData(self):
		i = Image.open(self.filename)
		info = i._getexif()
		if info:
			for tag, value in info.items():
				decoded = TAGS.get(tag, tag)
				if decoded == 'FNumber':
					(enumerator, denominator) = value
					self.fnumber = str(enumerator/denominator)

				elif decoded == 'ExposureTime':
					(unit, fraction) = value
					self.exposure = str(unit) + '/' + str(fraction)

				elif decoded == 'FocalLength':
					(enumerator, denominator) = value
					self.focal_length= str(enumerator/denominator)

				elif decoded == 'ISOSpeedRatings':
					self.iso = str(value)

				# else:
				# 	print str(decoded) + ' = ' + str(value)

		self.update()


	def create(self):
		print 'create'
		p_id = DB.addPhoto(self)


	def update(self):
		print 'create'
		p_id = DB.updatePhoto(self)





def get_all_photo_paths():
	photos = []
	
	for root, dirnames, filenames in os.walk('.'):
		for filename in fnmatch.filter(filenames, '*.jpg'):
			photos.append(os.path.join(root, filename))

	return photos


def add_photos_to_db(db):
	for photo_path in get_all_photo_paths():
		p = Photo()
		p.setFileName(photo_path)
		p.create()


def proc_exif_for_db_pics(db):
	for p in db.getAllPhotos():
		photo = Photo(p)

		photo.procExifData()


def help():
	print 'Usage:'


def main():
	db = DB

	if (len(sys.argv) <= 1):
		help()
		return

	if (sys.argv[1] == 'initDB'):
		db.initDB()
		return

	elif (sys.argv[1] == 'grab_photos'):
		db.initDB()
		add_photos_to_db(db)

	elif (sys.argv[1] == 'proc_exif'):
		proc_exif_for_db_pics(db)

	else:
		help()

	# if (getattr(p, sys.argv[1], help)() == False):
	# 	help()

if __name__ == "__main__":
	main()




