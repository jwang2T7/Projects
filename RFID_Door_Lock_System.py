#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader= SimpleMFRC522()

try:
	text=input("New Data:")
	print("Now place your tag to write")
	reader.write(text)
	print("Written")
finally:
	GPIO.cleanup()

#!/usr/bin/env python

from datetime import date
import datetime as dt

d1=date.today()
d2=dt.datetime.now()

Year=str(d1.year)
Month=str(d1.month)
Day=str(d1.day)

Hour=str(d2.hour)
Minute=str(d2.minute)
Second=str(d2.second)
Zero=str(0)
Record=print("Your Login Time is "+Hour+":"+Minute+":"+Second+" Your Login Date is "+Day+"-"+Zero+Month+"-"+Year) 
file=open('Records.txt','a')
file.write("\n"+Day+"-"+Zero+Month+"-"+Year+"  "+Hour+":"+Minute+":"+Second)

file1=open('Records.txt','r')
Ask=input("Do you want to see all of your login times (yes,no):")
if(Ask=='yes'):
	Records=file1.read()
	print(Records)

#!/usr/bin/env python

import datetime as dt

current_datetime= dt.datetime.now()

print(current_datetime.hour)
print(current_datetime.minute)
print(current_datetime.second)

#!/usr/bin/env python

from datetime import date
d1=date.today()
print(d1)
print(d1.month, d1.day, d1.year)
print(d1.weekday())

#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader= SimpleMFRC522()

try:
	id, text= reader.read()
	print(id)
	print(text)

finally:
	GPIO.cleanup()

#!/usr/bin/env python
import datetime as dt
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import date
d1=date.today()
d2=dt.datetime.now()

Year=str(d1.year)
Month=str(d1.month)
Day=str(d1.day)

Hour=str(d2.hour)
Minute=str(d2.minute)
Second=str(d2.second)
Zero=str(0)

file7=open("U1Password.txt","r+")
user1=file7.read()
file8=open("U2Password.txt","r+")
user2=file8.read()
reader= SimpleMFRC522()

id,text= reader.read()
one=id
two=str(text)
tag1=123144002073
tag2=1044624644778
if(one==tag1):
	Password=input("What is your password:")
	if(str(Password)==user1):
		print("Welcome Back,Jim!")
		Record=print("Your Login Time is "+Hour+":"+Minute+":"+Second+" Your Login Date is "+Day+"-"+Zero+Month+"-"+Year)
		file=open('User1_Record.txt','a')
		file.write("\n"+Day+"-"+Zero+Month+"-"+Year+"  "+Hour+":"+Minute+":"+Second)

		file1=open('User1_Record.txt','r')
		Ask=input("Do you want to see all of your login times (yes,no):")
		if(Ask=='yes'):
			Records=file1.read()
			print(Records)
		Change=input("Would you like to change your password (yes,no):")
		if(Change=="yes"):
                        reader= SimpleMFRC522()

                        try:
                                text1=input("New Password:")
                                print("Now place the tag on the reader to change the password")
                                reader.write(text1)
                                print("Written")
                                file8.truncate(0)
                                file8.write(text)

                        finally:
                                GPIO.cleanup()



	


elif(one==tag2):
	Password1=input("What is your password:")
	if(user2==Password1):
		print("Welcome Back,User 2!")
		Record1=print("Your Login Time is "+Hour+":"+Minute+":"+Second+" Your Login n Date is "+Day+"-"+Zero+Month+"-"+Year)
		file3=open('User2_Record.txt','a')
		file3.write("\n"+Day+"-"+Zero+Month+"-"+Year+"  "+Hour+":"+Minute+":"+Second)

		file4=open('User2_Record.txt','r')
		Ask1=input("Do you want to see all of your login times (yes,no):")
		if(Ask1=='yes'):
			Records1=file4.read()
			print(Records1)
		Change=input("Would you like to change your password (yes,no):")
		if(Change=="yes"):
                        reader= SimpleMFRC522()

                        try:
                                text1=input("New Password:")
                                print("Now place the tag on the reader to change the password")
                                reader.write(text1)
                                print("Written")

                        finally:
                                GPIO.cleanup()



file7.truncate(0)
file7.write(text)


