import math

p = 499
q = 547
a = -57
b = 52
X = 159201
n = p*q

message = int('10011100000100001100', 2)
print "Plaintext:\t" + bin(message)

def xor(bool1, bool2):
	return (bool1 != bool2)

def encrypt(msg, seed):
	k = int(math.floor(math.log(n, 2)))
	h = int(math.floor(math.log(k, 2)))
	numblocks = len(bin(msg))/h
	ctext = 0
	x_i = seed
	for i in range(numblocks-1, -1, -1):
		#x_i = x_i-1^2 % n
		x_i = pow(x_i, 2)%n
		#Create a bitmask to format m_i and p_i
		bitmask = 1 << h
		bitmask = bitmask -1
		#calculate m_i using the subblocks
		subblock = msg >> (h*i)
		m_i = subblock & bitmask
		p_i = x_i & bitmask
		#create the cipher subblock using p_i XOR m_i
		c_i = p_i ^ m_i
		ctext = ctext << h
		ctext = ctext | c_i
	#return the ciphertext, x_t+1, and t
	x_i = pow(x_i, 2)%n
	return ctext, x_i, numblocks

def decrypt(msg, x_t, t):
	k = int(math.floor(math.log(n, 2)))
	h = int(math.floor(math.log(k, 2)))
	#computer d1, d2, u, v, and x_0
	d1 = pow(((p+1)/4), t+1)%(p-1)
	d2 = pow(((q+1)/4), t+1)%(q-1)
	u = pow(x_t, d1)%p
	v = pow(x_t, d2)%q
	x_0 = (v*a*p + u*b*q)%n
	ptext = 0
	x_i = x_0
	#Repeat the loop from the encrypt function
	for i in range(t-1, -1, -1):
		#x_i = x_i-1^2 % n
		x_i = pow(x_i, 2)%n
		#Create a bitmask to format c_i and p_i
		bitmask = 1 << h
		bitmask = bitmask -1
		#calculate c_i using the subblocks
		subblock = msg >> (h*i)
		c_i = subblock & bitmask
		p_i = x_i & bitmask
		#create the cipher subblock using p_i XOR c_i
		m_i = p_i ^ c_i
		ptext = ptext << h
		ptext = ptext | m_i
	return ptext


encryptedmessage, x_t, t = encrypt(message, X)
print "Ciphertext:\t" + bin(encryptedmessage)
decryptedmessage = decrypt(encryptedmessage, x_t, t)
print "" + bin(encryptedmessage) + " after decryption is " + bin(decryptedmessage)
print "Message before:\t" + bin(message)
print "Message after: \t" + bin(decryptedmessage) 