#!/usr/bin/python

import os
import sys
import argparse
import urllib
from subprocess import Popen, PIPE

try:
    import imdb
except:
    print """

* IMDbPY needed 

(python-imdbpy from apt-get not working)

(Use dev version from: https://github.com/alberanid/imdbpy)

"""
    sys.exit(2)

version = '0.8'
USE_EXT = ('mp4', 'm4v', 'mkv')
exc_file = 'ilxr_excludes.txt'

i = imdb.IMDb()

def get_excludes(path):
#  print "sys.path is: ", sys.path[0]
#  print "getcwd is: ", os.getcwd()
#  print "path is: ", path
  if sys.path[0] != os.getcwd():
#    pf = path + '/'
    pf = sys.path[0] + '/'
  else:
    pf = ''
  efile = sys.path[0]+'/'+exc_file
  if os.path.exists(efile):
    print "Using excludes file: ", efile
    if path == '.':
      data = [path + '/' + line.strip() for line in open(efile, 'r')]
    else:
      data = [pf + line.strip() for line in open(efile, 'r')]
  else:
    print "Excludes file not found."
    data = ''
  return data


def get_titles (path):
  titleslist = []
  xlist = get_excludes(path)
  print "Excluding: ", xlist
  for dirName, subdirList, fileList in os.walk(path):
    print('directory: %s' % dirName)
    for fname in fileList:
        f = fname.rsplit('.',1)
        name = f[0]
        ext = f[1]
        if "]" in name:
           newname = name.split("] ",1)[1]
        else:
           newname = name
        if ext not in USE_EXT:
                continue
        fxml = name + ".xml"
        fjpg = name + ".jpg"
        dirPath = dirName.rsplit(path,1)[1]
#        print "dirPath: ", dirPath
#        print "dirName: ", dirName
        if dirName not in xlist:
#          print dirName, fname, newname, fxml, fjpg, dirPath
          titleslist.append((dirName, fname, newname, fxml, fjpg, dirPath))
    titleslist.sort()
  return titleslist


def jpgdownload (mid,jf):
    j = i.get_movie(mid)
    try:
      url = j['full-size cover url']
      if url is not None:
        wFile = urllib.urlopen(url)
        jfile = str(jf).encode('ascii','ignore')
        localFile = open(jfile,'w')
        localFile.write(wFile.read())
        wFile.close()
        localFile.close()
        print "...downloading jpg"
        print "...resizing jpg"
        cmd = ["convert", jfile, "-resize", "62400@", jfile]
        p = Popen( cmd, stdout=PIPE, stdin=PIPE)
        (stdout, stderr) = p.communicate()
        if stderr is not None:
          print stderr
      else:
        print "no full-size cover"
    except:
      print "error downloading cover"
      pass
    

def get_imdb_id (qid):
    s_result = i.search_movie(qid)
    id = 0
    for movie in s_result:
     print str(id)+' - '+movie['long imdb title']
     id = id + 1
    print
    response = raw_input('Which movie?  Enter the movie id, or s to skip, or q to quit.'  )
    if "q" in response:
     sys.exit(0)
    elif "s" in response:
     m1 = None
    else:
     m = s_result[int(response)]
     m1 = m.movieID
    return m1


def get_series_imdb_id (sid):
    m = i.get_movie(sid)
    m['kind']
    i.update(m,'episodes')
    print
    gid = 1
    for s in range(1,len(m['episodes'])+1):
     print str(gid)+' - Season '+str(s)
     gid = gid + 1
    print
    response = raw_input('Which season?  Enter the season id, or s to skip, or q to quit. '  )
    if "q" in response:
     sys.exit(0)
    elif "s" in response:
     mm = None
    else:
     mm = m['episodes'][int(response)]
    return mm


def list_series_imdb_id (mm,ef):
    id = 1
    print "Number of episodes: ", len(mm)
    print
    for movie in range(1,len(mm)+1):
      try:
        print str(id)+' - '+mm[int(movie)]['title']
      except:
        print str(id)+' - unknown'
        pass
      id = id + 1
    print
    print "--------------------"
    print ef
    print "--------------------"
    response = raw_input('Which episode?  Enter the episode id, or s to skip, or q to quit. '  )
    if "q" in response:
     sys.exit(0)
    elif "s" in response:
     m2 = None
    else:
     m1 = mm[int(response)]
     m2 = m1.movieID
    return m2


def writeXMLoutput (xml_dict,fil):
    myFile = open(fil, 'w')
    myFile.write(xml_dict['vid_beg']+'\n')
    myFile.write(xml_dict['title']+'\n')
    myFile.write(xml_dict['year']+'\n')
    myFile.write(xml_dict['genre']+'\n')
    myFile.write(xml_dict['mpaa']+'\n')
    myFile.write(xml_dict['director']+'\n')
    myFile.write(xml_dict['actors']+'\n')
    myFile.write(xml_dict['description']+'\n')
    myFile.write(xml_dict['length']+'\n')
    myFile.write(xml_dict['vid_end']+'\n')
    myFile.close()


def showXMLoutput (xml_dict,fil):
    print "--------------------"
    print "should write to: ", fil
    print "--------------------"
    print xml_dict['vid_beg']
    print xml_dict['title']
    print xml_dict['year']
    print xml_dict['genre']
    print xml_dict['mpaa']
    print xml_dict['director']
    print xml_dict['actors']
    print xml_dict['description']
    print xml_dict['length']
    print xml_dict['vid_end']


def create_xml (imdb_id):
    xml_dict = {'vid_beg':'<video>'}
    xml_dict['title'] = '<title></title>'
    xml_dict['year'] = '<year></year>'
    xml_dict['genre'] = '<genre></genre>'
    xml_dict['mpaa'] = '<mpaa></mpaa>'
    xml_dict['director'] = '<director></director>'
    xml_dict['actors'] = '<actors></actors>'
    xml_dict['description'] = '<description></description>'
    xml_dict['length'] = '<length></length>'
    xml_dict['vid_end'] = '</video>'
#
    if imdb_id is not None:
        m = i.get_movie(imdb_id)
        xml_dict['title'] = "<title>"+m['title']+"</title>"
        try:
          if args.year:
            xml_dict['year'] = "<year>"+args.year+"</year>"
          else:
            xml_dict['year'] = "<year>"+str(m['year'])+"</year>"
        except:
          pass
        try:
          if args.genre:
            xml_dict['genre'] = "<genre>"+args.genre+"</genre>"
          else:
            xml_dict['genre'] = "<genre>%s</genre>" %', '.join(m.get('genre'))
        except:
          pass
        try:
          if args.mpaa:
            xml_dict['mpaa'] = "<mpaa>"+args.mpaa+"</mpaa>"
          else:
            for region in m['certificates']:
              if region.split(':')[0]=='USA':
                xml_dict['mpaa'] = "<mpaa>"+region.split(':')[1].encode()+"</mpaa>"
        except:
          pass
        try:
          xml_dict['director'] = "<director>%s</director>" % ', '.join([director.get('name') for director in (m.get('director') or [])])
        except:
          pass
        try:
          if args.actors:
            xml_dict['actors'] = "<actors>"+str(args.actors)+"</actors>"
          else:
            actorList = ''
            for actor in [0,1,2]:
              actorList = actorList+str(m['actors'][actor])+', '
            xml_dict['actors'] = "<actors>"+actorList[0:-2]+"</actors>"
        except:
          pass
        try:
          plot = m['plot outline'].replace(u' \xbb', u'').encode()
          plot = plot.replace(' |', '')
          xml_dict['description'] = "<description>"+plot+"</description>"
        except:
          pass
        try:
          if args.length:
            xml_dict['length'] = "<length>"+args.length+"</length>"
          else:
            xml_dict['length'] = "<length>"+m['runtime'][0]+"</length>"
            for utime in m['runtime']:
              if utime.split(':')[0]=='USA':
                xml_dict['length'] = "<length>"+utime.split(':')[1].encode()+"</length>"
        except:
          pass
    return xml_dict  


def pullittogether(mmm,l):
    if args.series:
      if mmm is None:
        sid = get_imdb_id(args.series)
        mmm = get_series_imdb_id(sid)
      imdb_id = list_series_imdb_id(mmm,l[2])
    else:
      imdb_id = get_imdb_id(l[2])
    if imdb_id is not None:
      xml_dict = create_xml(imdb_id)
      if args.xml == 'show':
        print "show xml only"
        showXMLoutput(xml_dict,l[0]+'/'+l[3])
      elif args.xml == 'write':
        print "write xml only"
        writeXMLoutput(xml_dict,l[0]+'/'+l[3])
      else:
        print "both show and write xml"
        showXMLoutput(xml_dict,l[0]+'/'+l[3])
        writeXMLoutput(xml_dict,l[0]+'/'+l[3])
      if args.jpg:
        jfile = l[0]+'/'+l[4]
        jpgdownload(imdb_id,jfile)
    return mmm


def main():
    mmm = None
    print "directory to scan is: ", args.dirfile
    thelist = get_titles(args.dirfile)
    for l in thelist:
       print "--------------------"
       print l[2]
       print "--------------------"
       xfile = l[0]+'/'+l[3]
       if os.path.isfile(xfile):
         if args.new:
           continue
         else:
           with open(xfile) as f: 
             print f.read()
           print "--------------------"
           response = raw_input('Change XML file? Enter y to change, or q to quit, or enter to continue without changing.'  )
           if "q" in response:
             sys.exit(0)
           elif "y" in response:
             mmm = pullittogether(mmm,l)
             continue
           else:
             continue
       pullittogether(mmm,l)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create and maintain xlm files for Roksbox.', epilog='examples: ilxr.py "DIR", ilxr.py -s "Archer" "DIR"')
    parser.add_argument('dirfile', metavar='DIR', type=str, nargs='?', help='quoted movie directory', default='.')
    parser.add_argument('-x','--xml', action='store', type=str, help='[write|show|both] xml files', choices=['write','show','both'], default='write')
    parser.add_argument('-n','--new', action='store_true', help='only do movies without xml files')
    parser.add_argument('-j','--jpg', action='store_true', help='download jpg poster of video and resize with convert')
    parser.add_argument('-s','--series', action='store', help='quoted series name')
    parser.add_argument('-l','--length', action='store', help='overide imdb with "quoted" length')
    parser.add_argument('-g','--genre', action='store', help='overide imdb with "quoted" genre')
    parser.add_argument('-y','--year', action='store', help='overide imdb with "quoted" year')
    parser.add_argument('-m','--mpaa', action='store', help='overide imdb with "quoted" mpaa')
    parser.add_argument('-a','--actors', action='store', help='overide imdb with "quoted" actors')
    args = parser.parse_args()

    main()
