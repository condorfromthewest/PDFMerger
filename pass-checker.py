import requests
import hashlib

#the API uses k-anonimity method, thus only requires the first 5 characters of the hashed password
def req_api_data(query_char):
    ''' Connects with the website API and runs a request for specific character API information.
    '''
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}. Check API and try again.')
    return res

def pwned_api_check(password):
    '''Creates a hash from the user inputed password and then calls get_leak_counts function
    to check password for possible vulnerabilities.
    '''
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail_char = sha1password[:5], sha1password[5:]
    response = req_api_data(first5_char)
    return get_pass_leak_counts(response, tail_char)
    
def get_pass_leak_counts(hashes, hash_to_check):
    '''Runs a query comparing the first 5 characters from the hash with all possible tail characters that 
    match said first 5 characters. Returns a printed list with all tail characters from the hash followed by a 
    count of how many times they appear in the pwned database.
    '''
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
    #check my tail_char for appearance in the full tail character list
        if h == hash_to_check:
            return count
    return 0

def main(args):
    ''' Runs the API request and query from user-inputed passwords. Returns a print of the password followed by 
    the count, if it appears in the database, or a confirmation that it has not been pwned.
    '''
    for password in args:
        count = pwned_api_check(password)
        if count:
            a = f'The password {password} was found {count} times. '
            b = 'Perhaps you should check your password!'
            print(a+b)
        else:
            print(f'The password {password} was not found. Good!')
    print('All done.')
    print()

if __name__ == '__main__':
    print('Enter the passwords you wish to check. To start the analysis, press "enter":')
    list =[] 
    while True:
        passw = input()
        if passw == '':
            break
        else:
            list.append(passw)
    main(list)
