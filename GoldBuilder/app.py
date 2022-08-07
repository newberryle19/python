from app.func import *
import pandas as pd
from app.user import User


'''
fpath = 'var/raw_csv/April.csv'
tpath = path.basename(fpath)
q = path.splitext(tpath)[0]
x = import_csv_file(fpath)
print (tpath)
print(q)
print (x.name)
x = format_csv_file(x)
print (x.columns)
'''

'''
m=0
for i in x['Transaction Ammount']:
    if float(i) < 0:
        print(str(x['Transaction Ammount'][m]) + ' ' + x['Transaction source'][m])
    m +=1
    
'''    

create_user_base()
user = User()
print (user.username)
user.login_user()
print (user.fname)
print (user.lname)
print (user.username)
print (user.user_formated_dir)
print (user.user_raw_dir)

#user.create_user()
#print (user.fname)


#x.to_csv('static/user_data.csv', index=False)