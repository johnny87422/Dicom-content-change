import pydicom
import os

for i in os.listdir():
    if i[-4:] == '.dcm':
        ds = pydicom.dcmread(i)
        break
for name in ds.dir():
    print(name)
    print("")


