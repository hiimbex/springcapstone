''' For converting openssl rsa output to python integers'''

# Function argument is the name of a file containing an integer
# as it is represented in the output of openssl rsa, e.g.
#
# 00:a2:58:be:43:0c:af:2a:76:3a:13:1b:34:e7:dc:
# 77:c1:c6:5e:81:7b:bf:46:c2:0a:56:38:0a:ef:9d:
# 54:e7:df:95:77:c9:5a:e3:d1:25:52:32:ac:e7:8b:
# 37:8f:4e:7c:91:80:ca:93:ae:0a:80:bd:25:59:4c:
# 23:a2:1c:73:2a:d7:6b:7f:4d:6d:9c:37:57:a3:e0:
# 38:37:7b:c3:fd:4f:0d:b1:a2:17:cb:34:b8:24:56:
# cf:11:51:f0:e3:9b:20:65:71:a6:2d:1e:89:e1:04:
# 93:09:8d:b4:75:31:7a:d2:62:b7:6e:2d:b3:6e:f6:
# be:d4:27:13:b5:5c:98:c7:f9
#

import re
def export_in_decimal(filename):
    with open(filename) as f:
        s = f.read()

    s = re.sub('[:\s]','',s)
    print int(s,16)
    return int(s,16)

export_in_decimal('mod')
