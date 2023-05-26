import argparse
# import bcrypt
from passlib.hash import bcrypt

def hash_password(password):
    hash_pwd = bcrypt.using(rounds=12, ident="2y").hash(args.pwd)
    return hash_pwd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TE Gateway Config Tool [TECT]")
    # parser.add_argument('--product_id', dest='product_id', type=str, help='Add product_id')
    parser.add_argument('-u', '--username', dest='uname', type=str, help='username')
    parser.add_argument('-p', '--password', dest='pwd', type=str, help='Password')
    args = parser.parse_args()
    print(args.uname, args.pwd)
    passwd = f"{args.pwd}".encode()

    hash_pwd = hash_password(args.pwd)
    print(hash_pwd)
    print(f'INSERT into radius.radcheck (username,attribute,op,value) values("{args.uname}", "Crypt-Password", ":=", "{hash_pwd}");')
    # hashed = bcrypt.hashpw(passwd, salt)
    # print(hashed)
    # if bcrypt.checkpw(passwd, hashed):
    #     print("match")
    # else:
    #     print("does not match")
        