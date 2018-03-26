ilxr.py
=======

Latest version = 1.6

**Python 3 is now required!**

This python script will search imdb for information and save in a format compatible with [Roksbox](http://wilddtech.com/roksbox/home/).

It interactively creates individual xml files for each movie.

It is used mainly on Linux, but should work on other OSes.

Quote from Roksbox:
>Roksbox is a channel on the Roku Digital Video Player that gives you the ability to play your own videos and movies, listen to your own music, and show your own photographs on your television screen.

ilxr.py will search movies or series. If it finds an existing xml file with the same name as the video, it will skip the video.
If using the '-s' (--series) option, ilxr.py will ask for the series name, then the season, then the episode.
So it is best to set your seasons up in seperate folders.

By default, it will take a directory and search imdb for each video and ask you to choose the correct one.

###IMDbPY (required) 

**must be the latest version of python-imdbpy**

###Imagemagick (optional)

If you use the -j option, imagemagick is required, because it uses convert and resizes the image to a specified width.

Examples
=======

```
$ ./ilxr.py --help
usage: ilxr.py [-h] [-v] [-x {write,show,both}] [-r] [-j JPG] [-s SERIES]
               [-l LENGTH] [-g GENRE] [-y YEAR] [-m MPAA] [-a ACTORS] [-d]
               [DIR]

Create and maintain individual xml files for Roksbox.

positional arguments:
  DIR                   quoted movie directory

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -x {write,show,both}, --xml {write,show,both}
                        [write|show|both] xml files
  -r, --redo            do all movies (defaults to movies without xml files)
  -j JPG, --jpg JPG     download jpg poster and resize with convert (-j 200)
  -s SERIES, --series SERIES
                        quoted series name (-s "Archer")
  -l LENGTH, --length LENGTH
                        overide imdb with "quoted" length
  -g GENRE, --genre GENRE
                        overide imdb with "quoted" genre
  -y YEAR, --year YEAR  overide imdb with "quoted" year
  -m MPAA, --mpaa MPAA  overide imdb with "quoted" mpaa
  -a ACTORS, --actors ACTORS
                        overide imdb with "quoted" actors
  -d, --debug           print variables for debugging

examples: ilxr.py "DIR", ilxr.py -s "Archer" "DIR/Season"

```

```
$ ./ilxr.py transit
directory to scan is:  transit
directory: transit
directory: transit/shorts
--------------------
Big Buck Bunny
--------------------
0 - Big Buck Bunny (2008)
1 - Buck Rogers in the 25th Century (1979) (TV)
2 - Uncle Buck (1989)
3 - Bunny Lake Is Missing (1965)
4 - "The Big Bang Theory" (2007)
5 - "Big Brother (II)" (2000)
6 - Big Fish (2003)
7 - Buck and the Preacher (1972)
8 - "Big Brother Brasil" (2002)
9 - "Big Brother (III)" (2000)
10 - Big Daddy (1999)
11 - The Great Buck Howard (2008)
12 - Big Mommas: Like Father, Like Son (2011)
13 - Big Momma's House (2000)
14 - Big Momma's House 2 (2006)
15 - The Big Lebowski (1998)
16 - Big Stan (2007)
17 - The House Bunny (2008)
18 - The Bugs Bunny/Road-Runner Movie (1979)
19 - Big (1988)

Which movie?  Enter the movie id, or s to skip, or q to quit.
```

Example XML
======

```
<video>
<title>Maleficent</title>
<year>2014</year>
<genre>Action, Adventure, Family, Fantasy, Romance</genre>
<mpaa>PG</mpaa>
<director>Robert Stromberg</director>
<actors>Angelina Jolie, Elle Fanning, Sharlto Copley</actors>
<description>A vengeful fairy is driven to curse an infant princess, only to discover that the child may be the one person who can restore peace to their troubled land.</description>
<length>97</length>
</video>
```

###Notes

By default, ilxr.py will only work on following extensions: mp4, m4v, and mkv.
If you need others, add to the line in the python script:

USE_EXT = ('mp4', 'm4v', 'mkv')


Author
======

Joseph Archer (C) 2018


License
=======

The code is covered by the MIT.
