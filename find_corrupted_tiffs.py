import os
from glob import glob
from imghdr import what

target_path = r"*.TIF"

counter = 0
for tiff in glob(target_path):
 if os.path.getsize(tiff) <= 0 or what(tiff) is None:
  print("[Corruption detected] {0} has {1!s} bytes with filetype of {2}".format(os.path.basename(tiff), os.path.getsize(tiff), what(tiff)))
 counter += 1
 if counter % 100 == 0:
  print("Checked {0!s} files.".format(counter))

#ultra short version:
#print([os.path.basename(tiff) for tiff in glob(target_path) if what(tiff) is None])

#import glob, imghdr, os
#print([os.path.basename(tiff) for tiff in glob.glob(target_path) if imghdr.what(tiff) is None])
 
input("pause")
