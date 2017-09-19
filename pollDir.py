import os, time, subprocess
from subprocess import call
path_to_watch = "/home/pi/Documents/Scan/pdf"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
devnull = open(os.devnull, 'wb')

while 1:
  time.sleep (1)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
#  removed = [f for f in before if not f in after]
#  if added: print "Added: ", ", ".join (added)
  if added:
    for f in added:
      while 1:
        p1 = subprocess.Popen(["pdfinfo", "/home/pi/Documents/Scan/pdf/"+f],stderr=devnull,stdout=devnull)
        p1.wait()
        if p1.returncode == 0:
#          print "break"
          break
#        print p1.returncode
        time.sleep(1)
      call(["mv", "--backup=t", "/home/pi/Documents/Scan/pdf/"+f, "/home/pi/Documents/Scan/pdf/pyProcessed/"+f])
      time.sleep (1)
      call(["python", "tobi.py", "/home/pi/Documents/Scan/pdf/pyProcessed/"+f])
#print "added: " + f
#call(["mv", "/home/pi/Documents/Scan/pdf/" + , "/home/pi/Documents/Scan/pdf/pyProcessed/test1.pdf"])
#  if removed: print "Removed: ", ", ".join (removed)
  before = after
