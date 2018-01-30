import re
import pandas as pd
'''
We are going to write a script that turns the stata code into sql script

To do left:
    I need a better way to navigate through the file.
    I need to be able to load the data to sql
    load ms sql server on this machine

It would probably be better to read it all at once.  Maybe?
'''


table_name = "usa16_staging"
f = open("usa16_stata.txt", "r")
code_list = list()

def write_replace_code(name, func, val):
    code = name + " = " + name + func + val
    return code

def get_data_type (t):
    if t == "int":
        dt = "int"
    elif t == "double":
        dt = "float"
    else:
        dt = "varchar"

    return(dt)

x = 0
while x < 1:
    txt = f.readline()
    print(txt)
    if txt.startswith("quietly"):
        x = x+1

txt = f.readline()
txt = re.split(" *",txt)

while x < 2:
    # back to working on the sql code
    name = txt[2]
    start = re.split("-*",txt[3])[0]
    end = re.split("-*",txt[3])[1]

    dt = get_data_type(txt[1])
    # write the sql substring functions
    #   - note we could also add in data types here
    c = name + " =  cast(substring(X1," + start + ", " + str(int(end)-int(start)+1) + ") as " + dt + ")"
    code_list.append(c)
    print(len(code_list))
    # stop the loop when we see using
    txt = f.readline()
    txt = re.split(" *",txt)
    # add in the escape part
    if txt[1]=="using":
        x = x + 1

'''
now on to the "replace" section
'''
txt = f.readline() # we just need to skip a line
x = 0
while x < 1:
    txt = f.readline()
    txt = re.split(" *",txt)
    if txt[0] == "replace":
        name = txt[1]
        func = txt[4]
        val = txt[5].replace("\n","")
        c = write_replace_code(name, func, val)
        code_list.append(c)
    else:
        x = x + 1


for i in code_list:
    print(i)

'''
We are skipping the formatting section
'''
txt = f.readline()
txt = re.split(" *",txt)

while txt[0] != "label" and txt[1] != "define":
    txt = f.readline()
    txt = re.split(" *",txt)

'''
  now we want to make reference tables out of the label info
'''
variable = Series()
val = Series()
lbl = Series()
# now populate them
while len(f.readline()) > 0:
    txt = f.readline()
    txt = re.split(" *",txt)
    if txt[0]=="label":
        variable = variable.append(txt[2].replace("_lbl"))
        val = val.append(txt[3])
        lbl = lbl.append(txt[4])

# create the dataFrame with three
