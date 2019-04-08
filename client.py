import telnetlib

# HOST = "localhost"
HOST = "140.122.185.174"

tn = telnetlib.Telnet(HOST, 8081)
tn.read_until(b"---\n")
ciphertext = tn.read_until(b"---\n")[:-5]

print(ciphertext)

tn.read_until(b"What is your ciphertext?\n")

tn.write(ciphertext + b'\n')
ret = tn.read_until(b"padding\n")

if ret.find(b"invalid") != -1:
    print(b"invalid")
else:
    print(b"valid")
