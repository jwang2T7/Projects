

from cryptography.fernet import Fernet
import key_generator
import Encryption_Code
import sys 

user_input=input("Password: ")
password="1234567"

if user_input==password:
    key_generator
    file2=input("Which Document Would You Like to Encrypt: ")
    encoded1=file2.encode()
    file3=open(encoded1,'rb')
    message=file3.read()
    with open("Message.txt","wb") as f:
        f.write(message)
        f.close()
    Encryption_Code

else:
    sys.exit()

from cryptography.fernet import Fernet

file= open('key.txt', 'wb')
key=Fernet.generate_key()
file.write(key)
file.close()

from cryptography.fernet import Fernet

file= open('key.txt', 'rb')
key= file.read()
file.close()

message= "Hello World, My Name is Jim"
encoded= message.encode()

f=Fernet(key)
encrypted= f.encrypt(encoded)

file =open('encoded_message.txt', 'wb')
file.write(encrypted)
file.close()

f2= Fernet(key)
decrypted=f2.decrypt(encrypted)
orginal_message= decrypted.decode()
print(orginal_message)

from cryptography.fernet import Fernet
import user_interface

file= open('key.txt', 'rb')
key= file.read()
file.close()

with open("Message.txt", 'rb') as f:
    data= f.read()

fernet= Fernet(key)
encrypted= fernet.encrypt(data)

with open("AES_encoded_message.txt", 'wb') as f:
    f.write(encrypted)
    f.close()

with open('AES_encoded_message.txt', 'rb') as f:
    data= f.read()

fernet= Fernet(key)
decrypted= fernet.decrypt(data)

with open('final_message.txt', 'wb') as f:
    f.write(decrypted)
    f.close()

from cryptography.fernet import Fernet
file= open('key.txt', 'rb')
key= file.read()
file.close()
with open('AES_encoded_message.txt', 'rb') as f:
    data= f.read()

fernet= Fernet(key)
decrypted= fernet.decrypt(data)

with open('final_message.txt', 'wb') as f:
    f.write(decrypted)
    f.close()


