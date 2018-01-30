import re
import pandas as pd
'''
try creating a table first

I should make this a class

figure out a way to seperate out the sections
sections:
    1. variables and lengths
    2. replace
    3. label var: maybe these should just be csv's?
    4. label define
'''


table_name = "usa16_staging"
f = open("usa16_stata.txt", "r")
t_list = list()

x = f.readlines()
for txt in x:
    txt = txt.strip()
    txt = re.split(" *",txt)
    t_list.append(txt)

'''
working on the variables and lengths
'''
print(x[7])
