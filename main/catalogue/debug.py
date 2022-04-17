mydata = [
    {'data1': 123},
    {'data2': 124},
    {'data3': 120},
    {'data4': 127},
    {'data5': 118}
]

print(mydata.sort(key=lambda x: list(x.keys)))