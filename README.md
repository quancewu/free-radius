# radius
Build image
<pre>
docker compose build --no-cache
</pre>

Generate self-signed Certificate
<pre>
openssl req -x509 \
-subj '/C=TW/ST=Taiwan/L=Panchiao/CN=ccc.tc' \
-nodes -newkey rsa:2048 -keyout server.key -out server.crt -days 3650
</pre>

Get default setting from built image(service_hostname)
<pre>
./getconfig.sh radius_radius
</pre>

Start up
<pre>
docker-compose up -d
</pre>

Build radius database(password depend-on your-self)
<pre>
docker compose exec db mysql -h db -e "create database radius"
docker compose exec db mysql -h db -e "grant all on radius.* to 'radius'@'%' identified by 'hlOTg2ZmNk'"
</pre>

attach to radius container shell
<pre>
docker compose exec radius bash
</pre>

Check connection in mariadb is correct
-u<username> -p<password>

<pre>
mysql -uradius -phlOTg2ZmNk -h db
</pre>

input schema for default radius sql tables
<pre>
radius < /etc/freeradius/3.0/mods-config/sql/main/mysql/schema.sql
</pre>

Oneline script
<pre>
mysql -uradius -phlOTg2ZmNk -h db radius < /etc/freeradius/3.0/mods-config/sql/main/mysql/schema.sql
</pre>

Generate user/password php versoin
<pre>
./adduser.php devin test
INSERT into radius.radcheck (username,attribute,op,value) values("devin", "Crypt-Password", ":=", "$2y$10$TYKwxeU/RQ3B0l0oL4M1Eu7h8siL9b0qYltiGmmte3LjWnOrmDE/W");
</pre>

Generate user/password python3 versoin
<pre>
python3 adduser.py -u devin -p test
Username: devin | password: test
INSERT into radius.radcheck (username,attribute,op,value) values("devin", "Crypt-Password", ":=", "$2y$12$6NrhpKTKmnryyO0aNPoaI.LAnqFX9Hf6dXXDcGAqgwXmls0NdLtz2");
</pre>

login to mysql and put sql insert to sql
<pre>
docker-compose exec db mysql
</pre>

The relevant attribute instructions are provided below, and you can generate different grammars through testing.

<pre>
 Header	    Attribute		Description
       ------	    ---------		-----------
       {clear}	    Cleartext-Password	Clear-text passwords
       {cleartext}  Cleartext-Password	Clear-text passwords
       {crypt}	    Crypt-Password	Unix-style "crypt"ed passwords
       {md5}	    MD5-Password	MD5 hashed passwords
       {base64_md5} MD5-Password	MD5 hashed passwords
       {smd5}	    SMD5-Password	MD5 hashed passwords, with a salt
       {sha}	    SHA-Password	SHA1 hashed passwords
		    SHA1-Password	SHA1 hashed passwords
       {ssha}	    SSHA-Password	SHA1 hashed passwords, with a salt
       {sha2}	    SHA2-Password	SHA2 hashed passwords
       {sha224}     SHA2-Password	SHA2 hashed passwords
       {sha256}     SHA2-Password	SHA2 hashed passwords
       {sha384}     SHA2-Password	SHA2 hashed passwords
       {sha512}     SHA2-Password	SHA2 hashed passwords
       {ssha224}    SSHA2-224-Password	SHA2 hashed passwords, with a salt
       {ssha256}    SSHA2-256-Password	SHA2 hashed passwords, with a salt
       {ssha384}    SSHA2-384-Password	SHA2 hashed passwords, with a salt
       {ssha512}    SSHA2-512-Password	SHA2 hashed passwords, with a salt
       {nt}	    NT-Password 	Windows NT hashed passwords
       {nthash}     NT-Password 	Windows NT hashed passwords
       {md4}	    NT-Password 	Windows NT hashed passwords
       {x-nthash}   NT-Password 	Windows NT hashed passwords
       {ns-mta-md5} NS-MTA-MD5-Password Netscape MTA MD5 hashed passwords
       {x- orcllmv} LM-Password 	Windows LANMAN hashed passwords
       {X- orclntv} NT-Password 	Windows NT hashed passwords
</pre>

Modify clients.conf, for example: (secret can be modified, use the same secret when Wifi AP connects)
<pre>
client wifi {
	ipaddr = *
	secret = testing123
}
</pre>

Modify the sql file, and use the mysql database connection at the back end.
Because the connection is inside the container, there should be no need for encryption here.
<pre>
dialect = "mysql"
driver = "rlm_sql_${dialect}"

server = "db"
port = 3306
login = "radius"
password = "hlOTg2ZmNk"
# TLS
#	tls {
#		ca_file = "/etc/ssl/certs/my_ca.crt"
#		ca_path = "/etc/ssl/certs/"
#		certificate_file = "/etc/ssl/certs/private/client.crt"
#		private_key_file = "/etc/ssl/certs/private/client.key"
#		cipher = "DHE-RSA-AES256-SHA:AES128-SHA"
#		tls_required = yes
#		tls_check_cert = no
#		tls_check_cert_cn = no
#	}
</pre>


Restarting the container with the argument --remove-orphans seems to be fine at startup.
<pre>
docker-compose down --remove-orphans
docker-compose up -d
</pre>

Tail radius logs
<pre>
docker compose logs -f radius
</pre>

MacOS and iOS can only be connected through the Apple Configurator 2 description file.
https://apps.apple.com/tw/app/apple-configurator-2/id1037126344?mt=12

When connecting to Android, please select
TTLS & PAP

# radius
