import re

def strong_password(password):
    if len(password) < 8:
        return False
    patterns = [r'[a-z]', r'[A-Z]', r'[0-9]', r'[$#@]']
    if not all(re.search(pattern, password) for pattern in patterns):
        return False
    return True

if __name__ == '__main__':
    password = input('Enter password: ')
    if strong_password(password):
        print('Strong password')
    else:
        print('Weak password')