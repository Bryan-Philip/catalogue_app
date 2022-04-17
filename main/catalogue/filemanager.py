import re
import os
path_dataset = "./uploads/invoices/"
l = os.listdir(path_dataset)

print(l)

# def currentFiles():
for e in l:
    print(e)
    if os.path.isdir("./uploads/invoices/" + e):
        print('file exists')
        ll = os.listdir(path_dataset + e)
        for file in ll:
            print(file)
            if re.match(r".*\.xlsx$", file):
                print(e + '->' + file)
                    
# currentFiles()