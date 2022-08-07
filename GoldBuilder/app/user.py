import csv
from os import system, name as sysname, listdir, path, mkdir
import pandas as pd
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    
    def __init__(self):
        
        self.username = None
        self.fname = None
        self.lname = None
        self.user_raw_dir = None
        self.user_formated_dir = None
        self.password = None
        
        pass
    
    def create_user(self):
        '''Setup a new user for the application.'''
        static_dir = 'static/user_data.csv' #Static directory where user information is stored.
        existing_user_data = pd.read_csv(static_dir) #Set existing user information as a dataframe.
        base_dir ='user/' #Base Directory where user information is stored.
        self.fname = fname = input('First Name > ') # Collect users first name.
        self.lname = lname = input('Last Name > ') # Collect users last name.
        self.username = username = input('Username > ') # Collect username for the user.
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
        self.user_raw_dir = f'{user_dir}/raw_csv'
        self.user_formated_dir = f'{user_dir}/formated_csv'
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
        
        self.password = hash_pass = generate_password_hash(pass1, method='sha256')
        user_dict = {'Username':[username], 'First Name':[fname], 'Last Name':[lname], 'User Directory':[user_dir], 'Password Hash':[hash_pass]}
        new_user = pd.DataFrame(user_dict)
        add_user = pd.concat([existing_user_data, new_user], axis=0)    
        #This Line appends the new user to the existing user csv file.
        add_user.to_csv(static_dir, index=False)
        
    def login_user(self):
        registered_users = pd.read_csv('static/user_data.csv')
        username = input('Username > ')
        index = 0
        for i in registered_users['Username']:
            if i == username:
                print ('User found')
                password = getpass('Password > ')
                stored_password = registered_users['Password Hash'][index]
                index = index
                break
            else:
                index += 1
                
            
        
        good_pass = check_password_hash(stored_password,password) #Check stored password against entered password.
        
        if good_pass:
            self.username = username
            self.password = stored_password
            self.fname = registered_users['First Name'][index]
            self.lname = registered_users['Last Name'][index]
            self.user_formated_dir = f"{registered_users['User Directory'][index]}formated_csv"
            self.user_raw_dir = f"{registered_users['User Directory'][index]}raw_csv"
            print(f'{self.username} logged in.')
        else:
            print ('Password does not match')
        
        pass