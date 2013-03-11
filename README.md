# Photontistics

So this name... It derives from Photo + Python + Statistics. I know, it is
silly, but all names are.

The objective of this application is to store exif information about pictures
to help the photographer to check analytics like what focal lenght do I shoot
the most? Or do I need to keep this lens or should I get a better one for
the X kind of photos?

Today it only gets the following information out of the EXIF:

- FNumber
- Exposure
- ISO
- Focal Length

There are really more to come. It has the objectives of:

- Compile it to a file to be readed by HTML (csv?)
- Get more information about camera, lens, etc...


## How to

Right now you should execute in your photo root folder:

    $ ./photontistics.py grab_photos
    $ ./photontistics.py proc_exif

First step will gather all your pictures and put a pointer to it inside the
sqlite3 database. Step #2 will process exif information and save it to the
database.

Existing pictures are not saved again in grab photos. Removed ones are also
not removed. Those are to come.

## Requisites

This application is written in python, so it is supposed to work in any
system. There is a list of modules is uses that must be installed:

- PIL
