### Number Generator Dump
            
# for v in val:
#     if(v == '/' or v == ' ' or manage == len(val)-1):
#         if(manage == len(val)-1):
#             if(v != ' '):
#                 inner_number.append(v)
#         if(len(inner_number) <= 4):
#             if(v == '/'):
#                 # print(inner_number)
#                 print("numberlist")
#                 print(number_list)
#                 print("numberlist")
#                 if(len(number_list) == 0):
#                     number_list = list(inner_number)
#                 stack = number_list[counter-1]
#                 rel = stack[0:len(stack)-len(inner_number)]
#                 rel = ''.join(str(n) for n in rel)
#                 inner_number = ''.join(inner_number)
#                 inner_number = str(rel)+inner_number
#             elif(v == ' ' or v == '-' or v in numberstrings):
#                 if(len(number_list) == 0):
#                     inner_number = ''.join(inner_number)
#                     number_list.append(inner_number)
#                 stack = number_list[counter-1]
#                 rel = stack[0:len(stack)-len(inner_number)]
#                 rel = ''.join(str(n) for n in rel)
#                 inner_number = ''.join(inner_number)
#                 if(inner_number in codes):
#                     depend = list(inner_number+v)
#                     pass
#                 elif(len(inner_number) == 3):
#                     if(inner_number in TELEPHONES_VOID or inner_number == '254' or inner_number == '+254'):
#                         depend = list(inner_number+v)
#                         # print(depend)
#                         pass
#                     else:
#                         inner_number = str(rel)+inner_number
#                 elif(len(inner_number) == 4):
#                     if(inner_number in TELEPHONES):
#                         depend = list(inner_number+v)
#                         pass
#                     else:
#                         inner_number = str(rel)+inner_number
#                 else:
#                     inner_number = str(rel)+inner_number
#             print("required")
#             print(inner_number)
#             print(number_list)
#         conced = ''.join(str(n) for n in list(inner_number))
#         if(len(depend) == 0):
#             exist = ''
#             if(len(number_list) > 0):
#                 exist = number_list[counter-1]
#             if(conced != exist):
#                 number_list.append(conced)
#                 # print('-- numberlist --')
#                 # print(conced)
#                 # print(number_list)
#                 # print('-- end of numberlist --')
#                 counter += 1
#         else:
#             # print('depend')
#             print(depend)
#             pass
#         inner_number = list()
#     else:
#         if(len(depend) >= 1):
#             inner_number = depend
#             # print('inner number')
#             # print(inner_number)
#             depend = list()
#         else:
#             inner_number.append(v)
#     manage += 1
# return number_list

### End of Number Generator Dump


### Data Interpretor

# PRIME = load_workbook(filename = './documents/invoices/PRIME.xlsx')
# GARDEN = load_workbook(filename = './documents/invoices/GARDEN.xlsx')
# SIAN = load_workbook(filename = './documents/invoices/SIAN.xlsx')

# prime_sheet = PRIME['Sheet1']
# garden_sheet = GARDEN['70']
# sian_sheet = SIAN['Tea Broket Dtls excel Summary']

# prime_data = list()
# garden_data = list()
# sian_data = list()

# def generate_data(data, set_data, sheet):
    # counter = 0
    # for data in data.values():
    #     inner_counter = 0
    #     inner_dict = dict()
    #     for inner_data in data:
    #         if(sheet == "garden"):
    #             relation = getAliasRelation(garden_relation[inner_counter])
    #         elif (sheet == "prime"):
    #             relation = getAliasRelation(prime_relation[inner_counter])
    #         elif (sheet == "sian"):
    #             relation = getAliasRelation(sian_relation[inner_counter])
    #         if(relation != False):
    #             inner_dict[relation] = inner_data
    #         else:
    #             inner_dict[relation] = None
    #         inner_counter += 1
    #     set_data.append(inner_dict)
    #     counter += 1
    
# def init_garden():
#     bc = 0
#     inner = list()
#     endif_check = list()
#     for row in garden_sheet.values:
#         inner_counter = 0
#         if(len(endif_check) >= 3 and bc >= 5):
#             break
#         elif(bc >= 1):
#             if(bc > 5):
#                 garden_data[bc-6] = inner
#         bc += 1
#         inner = list()
#         endif_check = list()
#         for value in row:
#             if(inner_counter >= 0):
#                 if(value != None):
#                     if(bc == 5):
#                         garden_relation.append(value)
#                     inner.append(value)
#                 else:
#                     inner.append(None)
#                     endif_check.append(value)
#             inner_counter += 1
            
# def init_prime():
#     bc = 0
#     inner = list()
#     endif_check = list()
#     for row in prime_sheet.values:
#         inner_counter = 0
#         if(len(endif_check) >= 3 and bc >= 5):
#             break
#         elif(bc >= 1):
#             if(bc > 5):
#                 prime_data[bc-6] = inner
#         bc += 1
#         inner = list()
#         endif_check = list()
#         for value in row:
#             if(inner_counter >= 0):
#                 if(value != None):
#                     if(bc == 5):
#                         prime_relation.append(value)
#                     inner.append(value)
#                 else:
#                     inner.append(None)
#                     endif_check.append(value)
#             inner_counter += 1
            
# def init_sian(left_bound, top_bound, data_layer):
#     bc = 0
#     inner = list()
#     endif_check = list()
#     for row in sian_sheet.values:
#         inner_counter = 0
#         if(len(endif_check) >= 5 and bc >= 5):
#             break
#         elif(bc >= top_bound-1):
#             sian_data[bc-(top_bound-1)] = row[slice(left_bound-1, len(row))]
#         inner = list()
#         endif_check = list()
#         for value in row:
#             if(inner_counter >= left_bound-1):
#                 if(value != None):
#                     if(bc == data_layer-1):
#                         sian_relation.append(value)
#                     inner.append(value)
#                 else:
#                     inner.append(None)
#                     endif_check.append(value)
#             inner_counter += 1
#         bc += 1

        
# DataInterpretor.init_garden()
# DataInterpretor.init_prime()
# DataInterpretor.init_sian(1, 2, 1)
# DataInterpretor.generate_data(garden_data, garden_final, "garden")
# DataInterpretor.generate_data(prime_data, prime_final, "prime")
# DataInterpretor.generate_data(sian_data, sian_final, "sian")

# combined = prime_final + garden_final + sian_final

### End of Data Interpretor 