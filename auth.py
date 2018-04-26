import hashlib, uuid

def findUser(name):
	with open("users.txt", "r") as usrFile:
		for line in usrFile:
			line = line.split(" : ")
			print(line)
			if line[0].lower() == name.lower():
				return True
			else:
				continue
		return False; 

def checkPassword(name, pw):
	with open("users.txt", "r") as usrFile:
		for line in usrFile:
			line = line.split(" : ")
			print(line)
			if line[0].lower() == name.lower():
				if line[1] == pw:
					return True
				else:
					return False
			else:
				continue
		return False; 

def addUser(name, hash, salt):
	with open("users.txt", "a") as usrFile:
		name = name.lower().strip()
		usrFile.write("\n" + name + " : " + hash + " : " + salt)


def hashPW(pw, salt):
    return hashlib.sha512((pw + salt).encode('utf-8')).hexdigest()