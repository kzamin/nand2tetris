import re
from numpy import binary_repr

def dest(mDest):
	#return binary code of the dest mnemoic (string)
	#return 3 bits
	binaryCodeDest = ["A", "D", "M"]
	binaryCodeDest[0] = boolToBinary("A" in mDest)
	binaryCodeDest[1] = boolToBinary("D" in mDest)
	binaryCodeDest[2] = boolToBinary("M" in mDest)

	return ''.join(binaryCodeDest)

def comp(mComp):
	#return binary code of the comp mnemoic
	#return 7 bits ac1c2c3c4c5c6
	binaryCodeComp = ["a", "c1", "c2", "c3", "c4", "c5", "c6"]
	codesComp = {'0':  '0101010', 
				'1':  '0111111',
				'-1': '0111010',
				'D':  '0001100',
				'A':  '0110000', 
				'!D': '0001101',
				'!A': '0110001',
				'-D': '0001111',
				'-A': '0110011',
				'D+1':'0011111',
				'A+1':'0110111',
				'D-1':'0001110',
				'A-1':'0110010',
				'D+A':'0000010',
				'D-A':'0010011',
				'A-D':'0000111',
				'D&A':'0000000',
				'D|A':'0010101',
				#a=1
				'M'  :'1110000',
				'!M' :'1110001',
				'-M' :'1110011',
				'M+1':'1110111',
				'M-1':'1110010',
				'D+M':'1000010',
				'D-M':'1010011',
				'M-D':'1000111',
				'D&M':'1000000',
				'D|M':'1010101'}

	return codesComp[mComp]


def jump(mJump):
	#return binary code of the jump mnemoic
	#return 3 bits
	codesJump = {
		'null': '000',
		'JGT' : '001',
		'JEQ' : '010',
		'JGE' : '011',
		'JLT' : '100',
		'JNE' : '101',
		'JLE' : '110',
		'JMP' : '111'}

	return codesJump[mJump]
	

def boolToBinary(xBool):
	if xBool == True:
		return "1"
	else:
		return "0"

#------------------------------------------------------------------------

class SymbolTable(object):

	def __init__(self):
		#create new empty SymbolTable
		self.symbolTable = {}

	def addEntry(self, symbol, address):
		#add symbol, address pair to SymbolTable
		self.symbolTable[symbol] = address

	def contains(self, symbol):
		#does the table contain the given symbol
		#return boolean
		return symbol in self.symbolTable

	def getAddress(self, symbol):
		#return address associated with the symbol
		#return int
		return self.symbolTable[symbol]

#-----------------------------------------------------------------------

def destM(command):
	#returns dest mnemoic of current C instruction - 8 Poss
	#called when command type is C
	#return string
	if "=" in command:
		return command[:command.index("=")] 
	else: 
		return "000"

def compM(command):
	#returns comp mnemoic of current C instruction - 28 Poss
	#called when command type is C
	#return string
	if ("=" in command) and (";" in command):
		return command[command.index("=") + 1: command.index(";")]
	elif "=" in command:
		return command[command.index("=") + 1:]
	elif  ";" in command:
		return command[:command.index(";")] 

def jumpM(command):
	#return jump mnemoic of current C instruction - 8 Poss
	#called when command type is C
	#return string
	if ";" in command:
		return command[command.index(";") + 1:]
	else:
		return "null"

#------------------------------------------------------------------------

def convertDecimalToBinary(decimal):
	# can be 15 bits at most
	binaryValues = [16384, 8192, 4096, 2048, 2024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]
	returnArr = ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']
	currentVal = int(decimal)
	i = 0

	while i < len(binaryValues):
		if currentVal - binaryValues[i] >= 0:
			currentVal -= binaryValues[i]
			returnArr[i] = '1'
			i += 1
		else:
			returnArr[i] = '0'
			i += 1

	return ''.join(returnArr)

def dec_to_bin(x):
    return "{0:16}".format(x)

def sixteenBin(x):
	if len(x) != 16:
		while len(x) < 16:
			x = "0" + x


#------------------------------------------------------------------------

def commandType(command):
	#returns type of current command A_COMMAND, C_COMMAND, L_COMMAND
	#C A or L(psuedo command for (XxX))
	#dest=comp; jmp, @, ()
	i = 0
	while i < len(command):
		if command[i] != " ":
			firstChar = command[i]
			break
		else:
			i += 1

	if firstChar == "@":
		return "A_COMMAND"
	elif firstChar == "(":
		return "L_COMMAND"
	elif firstChar == "/" or firstChar == "S": # if comment or whitespace
		return "COMMENT"
	else:
		return "C_COMMAND"

#------------------------------------------------------------------------

def firstPass(fileAddress):
	with open(fileAddress, "r") as f:
		commands = list(f)

	c = 0
	i = 0
	ROM = 0
	symbolTableM = SymbolTable()
	acArr = []

	while c < len(commands):
		#commands[c] += ("\\n")
		commands[c] = commands[c].replace("\n", " SKIP")
		commandTypeF = commandType(commands[c]) # command type of each command

		if (commandTypeF == "A_COMMAND") or (commandTypeF == "C_COMMAND"):
			acArr.append(commands[c])
			ROM += 1

		if commandTypeF == "L_COMMAND":
			label = commands[c][commands[c].find("(")+1 : commands[c].find(")")]
			symbolTableM.addEntry(label, ROM) # willing to change to c if nesscary

		c += 1

	a=0

	while a < len(acArr):
		#if acArr[a].find("//") != -1:
			#acArr[a] = acArr[:acArr[a].find("/")]
		acArr[a] = acArr[a].replace("SKIP", "")
		try:
			acArr[a] = acArr[a][0:acArr[a].index("/")]
		except: 
			pass

		acArr[a] = re.sub(r'\s+', '', acArr[a])

		a+=1

	symbolTableM.addEntry("SP", "0")
	symbolTableM.addEntry("LCL", "1")
	symbolTableM.addEntry("ARG", "2")
	symbolTableM.addEntry("THIS", "3")
	symbolTableM.addEntry("THAT", "4")
	symbolTableM.addEntry("R0", "0")
	symbolTableM.addEntry("R1", "1")
	symbolTableM.addEntry("R2", "2")
	symbolTableM.addEntry("R3", "3")
	symbolTableM.addEntry("R4", "4")
	symbolTableM.addEntry("R5", "5")
	symbolTableM.addEntry("R6", "6")
	symbolTableM.addEntry("R7", "7")
	symbolTableM.addEntry("R8", "8")
	symbolTableM.addEntry("R9", "9")
	symbolTableM.addEntry("R10", "10")
	symbolTableM.addEntry("R11", "11")
	symbolTableM.addEntry("R12", "12")
	symbolTableM.addEntry("R13", "13")
	symbolTableM.addEntry("R14", "14")
	symbolTableM.addEntry("R15", "15")
	symbolTableM.addEntry("SCREEN", "16384")
	symbolTableM.addEntry("KBD", "24576")

	secondPass(fileAddress, symbolTableM, commands, acArr)

#------------------------------------------------------------------------

def secondPass(fileAddress, symbolTableM, commands, acArr):
	f = open(fileAddress[:len(fileAddress)-3] + "hack", "w+")
	c = 0

	while c < len(acArr):
		variableNum = 16
		if commandType(acArr[c]) == "C_COMMAND":
			f.write("111" + comp(compM(acArr[c])) + (dest(destM(acArr[c]))) + (jump(jumpM(acArr[c]))) + "\n" )
			# print(destM(acArr[c]))
			# print(jumpM(acArr[c]))
			# print(comp(compM(acArr[c])))
		elif commandType(acArr[c]) == "A_COMMAND":
			key = acArr[c][acArr[c].index("@") + 1:]
			# check symbol table first, then convert to binary
			# print(address)
			#print(symbolTableM.contains("R0"))

			if symbolTableM.contains(key):
				f.write("0" + str(binary_repr(int(symbolTableM.getAddress(key)), 15)) + "\n")
			elif key.isdigit(): 
				f.write("0" + str(binary_repr(int(key), 15)) + "\n")
			else:
				symbolTableM.addEntry(key, variableNum)
				variableNum += 1
				f.write("0" + str(binary_repr(int(symbolTableM.getAddress(key)), 15)) + "\n")


			# f.write(convertDecimalToBinary(acArr[c]))
		c = c + 1

	print(symbolTableM.symbolTable)
	f.close()
#------------------------------------------------------------------------

def main(fileAddress):
	firstPass(fileAddress)
	# print("\\n")
