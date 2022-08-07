import csv
from os import system, name as sysname, listdir, path, mkdir
import pandas as pd
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash

def create_user_base():
    '''Check if the required user base file exist and creates one if it does not exist.'''
    
    static_dir = 'static/user_data.csv' #Static location where user information is stored.
    isdir = path.exists(static_dir) #True if file exist, False if file does not exist.
    
    #If the file exist notify the user.
    if isdir:
        print (f'User file exist at \'{static_dir}\'.')
    #If the file does not exist, notify the user and create the file.    
    else:
        print('User file does not exist. Creating User File.')
        user_base = pd.DataFrame(columns=['Username','First Name','Last Name','User Directory','Password Hash'])
        user_base.to_csv(static_dir, index = False)
        print(f'User base file created at \'{static_dir}\'.')


def create_user():
    '''Setup a new user for the application.'''
    static_dir = 'static/user_data.csv' #Static directory where user information is stored.
    existing_user_data = pd.read_csv(static_dir) #Set existing user information as a dataframe.
    base_dir ='user/' #Base Directory where user information is stored.
    fname = input('First Name > ') # Collect users first name.
    lname = input('Last Name > ') # Collect users last name.
    username = input('Username > ') # Collect username for the user.
    user_dir = f'{base_dir}{username}/' #Specific directory where user information is stored at.
    isdir = path.exists(f'{user_dir}') #True if user directory exist False if it does not exist.
    
    # Check if the user has a directory, if not then create one for them
    if not isdir:
        print('User directory does not exist, attempting to create directory')
        mkdir(user_dir) #Create main directory.
        print(f'Directory created at {user_dir}')
        print(f'Attempting to create sub folders for {username}')
        mkdir(f'{user_dir}/raw_csv/') #Create sub folder for raw files.
        mkdir(f'{user_dir}/formated_csv/') #Create sub folders for formated files.
        print(f'Finished creating folders for {username}')
       
    pass1 = getpass('Password > ') #Collect a password from the user
    pass2 = getpass('Confirm Password > ') #Collect the password again to verify.
    
    #While loop checks if passwords match
    match = False
    while match == False:
        if pass1 != pass2:
            print ('Passwords do not match, try again')
            npass1 = getpass('Password > ')
            npass2 = getpass('Confirm Password > ')
            if npass1 == npass2:
                match = True
            else:
                match = False
        else:
            match = True
    
    hash_pass = generate_password_hash(pass1, method='sha256')
    user_dict = {'Username':[username], 'First Name':[fname], 'Last Name':[lname], 'User Directory':[user_dir], 'Password Hash':[hash_pass]}
    new_user = pd.DataFrame(user_dict)
    add_user = pd.concat([existing_user_data, new_user], axis=0)    
    #This Line appends the new user to the existing user csv file.
    add_user.to_csv(static_dir, index=False)
    
    
def login():
    pass


def hash_password(password):
    pass

def check_password_hash(password, hash):
    pass

def clear_screen():
    '''Quickly clear the screen on both windows, Mac, and Linux machines.'''
    # If loop checks if system is windows or unix.
    if sysname == 'nt':
        _=system('cls')
    else:
        _=system('clear')
        

def import_csv_file(fpath):
    '''Open a csv file so the program can access it'''
    #csv header:
    #"Date Posted","Date Completed","Transaction source","Transaction Ammount","Ending Balance"
    
    filename = path.basename(fpath)
    name = path.splitext(filename)[0]
    
    file = pd.read_csv(f'{fpath}', header=None)
    file.name = name

    return file


def export_csv_file(object, fpath):
    '''Export a dataframe object as a csv file to a given path'''
    file = pd.DataFrame(object)
    file.to_csv(f'{fpath}', index=False)
    print (f'File created at {fpath}')


def format_csv_file(csv):
    '''Format csv file to a format needed to work with, you may need to add or remove parts of this
    function depending on how your raw files are formated and what your desired output is'''
    
    #csv header used in import_csv() function:
    #"Date Posted","Date Completed","Transaction source","Transaction Ammount","Ending Balance"

    csv = pd.DataFrame(csv)
    
    csv.columns = ["Date Posted","Date Completed","Transaction source","Transaction Ammount","Ending Balance"]
    csv['Transaction source'] = csv['Transaction source'].map(convert_upper)
    csv['Transaction Ammount'] = csv['Transaction Ammount'].replace({'\$' : ''}, regex=True)
    #july['Transaction Ammount'] = july['Transaction Ammount'].replace({'\-' : ''}, regex=True)
    #july['Transaction Ammount'] = july['Transaction Ammount'].replace({'\+' : ''}, regex=True)
    csv['Ending Balance'] = csv['Ending Balance'].replace({'\$' : ''}, regex=True)
    #july['Ending Balance'] = july['Ending Balance'].replace({'\+' : ''}, regex=True)
    csv['Transaction source'] = csv['Transaction source'].replace({'POINT OF SALE WITHDRAWAL' : 'Source '}, regex=True)
    
    return csv


def bulk_format(indir='./var/raw_csv', outdir='./var/formated_csv/'):
    
    indir = listdir(f'{indir}')
    outdir = outdir
    
    for i in indir:
        print ('Raw csv file found ' + f'{i}')
        file = import_csv_file(f'./var/raw_csv/{i}', i)
        print ('Raw csv file imported.')
        print ('Attempting to format csv file.')
        file = format_csv_file(file)
        print ('Raw csv file has been formated.')
        print ('Now attempting to export formated csv file.')
        export_csv_file (file, f'{outdir}{i}')
        
        
def find_charge(object):
    object = pd.DataFrame(object)
    m=0
    for i in object['Transaction source']:
        if float(object['Transaction Ammount'][m]) < 0:
            print (f"{object['Transaction Ammount'][m]}  {object['Transaction source'][m]}")
        m+=1
        
def find_deposit(object):
    object = pd.DataFrame(object)
    m=0
    for i in object['Transaction source']:
        if float(object['Transaction Ammount'][m]) > 0:
            print (f"{object['Transaction Ammount'][m]}  {object['Transaction source'][m]}")
        m+=1
        
def convert_upper(text):
    txt = str(text)
    return txt.upper()