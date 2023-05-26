import argparse

from passlib.hash import bcrypt

def hash_password(password):
    hash_pwd = bcrypt.using(rounds=12, ident="2y").hash(args.pwd)
    return hash_pwd


def generate_sql_cmd(uname, pwd):
    print(f"Username: {uname} | password: {pwd}")
    passwd = f"{pwd}".encode()
    hash_pwd = hash_password(args.pwd)
    print(f'INSERT into radius.radcheck (username,attribute,op,value) values("{uname}", "Crypt-Password", ":=", "{hash_pwd}");')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="simple tools for generate hash password for radius server db")
    parser.add_argument('-u', '--username', dest='uname', type=str, help='username')
    parser.add_argument('-p', '--password', dest='pwd', type=str, help='Password')
    args = parser.parse_args()
    if (args.uname is None) & (args.pwd is None):
        print("parameter -u -p not found")
    else:
        generate_sql_cmd(args.uname, args.pwd)

        