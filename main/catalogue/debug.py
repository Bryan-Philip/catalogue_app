# mydata = [
#     {'data1': 123},
#     {'data2': 124},
#     {'data3': 120},
#     {'data4': 127},
#     {'data5': 118}
# ]

# print(mydata.sort(key=lambda x: list(x.keys)))

def replaceResale(v):
    resalestr = ["Resale", "resale", "RESALE"]
    for resale in resalestr:
        if resale in str(v):
            head, sep, tail = str(v).partition(resale)
            head += sep
            return str(head).replace(" ", "").replace("-Resale", "").replace("-resale", "").replace("-RESALE", "").replace("Resale", "").replace("resale", "").replace("RESALE", "")
        else:
            return v
