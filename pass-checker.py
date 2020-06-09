import requests
import hashlib

#the API uses k-anonimity method, thus only requires the first 5 characters of the hashed password
def req_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}. Check API and try again.')
    return res

#Aquí creo mi hash password a partir de mi input 'password' y luego llamo a mi función get_leak_counts
#para ver si mi password ya se encuentra en el sistema del API y ver cuántas veces fue vulnerada
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail_char = sha1password[:5], sha1password[5:]
    response = req_api_data(first5_char)
    #print(response.text) me muestra todos los endings coincidentes con mis first5_char, y cuantas veces aparece
    return get_pass_leak_counts(response, tail_char)
    
#Esta función me devuelve todos los tail_char de hash passwords que coinciden con mis primeros
#first5_char. voy a ver una impresión de listas con todos los tail_char en [0] y la cuenta de cuántas veces
#aparecen en [1]
def get_pass_leak_counts(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
    #con este if evaluo a mi tail_char para ver si aparece en la lista
        if h == hash_to_check:
            return count
    return 0

def main(args):
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