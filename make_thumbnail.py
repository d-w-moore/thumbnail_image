import os, sys
import json
import datetime
from PIL import Image


# capture incoming parameters
size_str = sys.argv[1]
src_name = sys.argv[2]
dst_name = sys.argv[3]
dst_coll = sys.argv[4]

# build size array
size_vals = size_str.split('x')
size = int(size_vals[0]), int(size_vals[1])

# generate thumbnail
try:
    im = Image.open(src_name)
    im.thumbnail(size)
    im.save(dst_name, im.format)
except IOError:
    print("cannot create thumbnail for: " + src_name)
    sys.exit()
# create metadata and build json representation for moarlock
avu_list = []

avu = {}
avu['attribute'] = 'source_image'
avu['value'] = os.path.basename(src_name)
avu['unit'] = ''
avu['irodsPath'] = os.path.basename(dst_name)
avu['action'] = 'ADD'
avu_list.append(avu)

avu = {}
avu['attribute'] = 'time_stamp'
avu['value'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
avu['unit'] = ''
avu['irodsPath'] = os.path.basename(dst_name)
avu['action'] = 'ADD'
avu_list.append(avu)

md_manifest = {}
md_manifest['operation'] = avu_list
md_manifest['failureMode'] = 'FAIL_FAST'
md_manifest['parentIrodsTargetPath'] = dst_coll

# write out manifest for moarlock
with open('/dst/mdmanifest.json', 'w') as outfile:
    json.dump(md_manifest, outfile, sort_keys=True, indent=4, separators=(',', ': '))
