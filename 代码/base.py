s = "HIJKLMNOPQRSTUVWXYZABCDEFGhijklmnopqrstuvwxyzabcdefg0123456789+/"    #码表

def My_base64_encode(inputs):
	bin_str = []
	for i in inputs:
		x = str(bin(ord(i))).replace('0b', '')
		bin_str.append('{:0>8}'.format(x))
	#print(bin_str)
	outputs = ""
	nums = 0
	while bin_str:
		temp_list = bin_str[:3]
		if(len(temp_list) != 3):
			nums = 3 - len(temp_list)
			while len(temp_list) < 3:
				temp_list += ['0' * 8]
		temp_str = "".join(temp_list)
		#print(temp_str)
		temp_str_list = []
		for i in range(0,4):
			temp_str_list.append(int(temp_str[i*6:(i+1)*6],2))
		#print(temp_str_list)
		if nums:
			temp_str_list = temp_str_list[0:4 - nums]
			
		for i in temp_str_list:
			outputs += s[i]
		bin_str = bin_str[3:]
	outputs += nums * '='
	print("Encrypted String:\n%s "%outputs)

print("-------input 'ys' to encode-------")	

sr = input("Please input!\n")
if(sr == "ys"):
	input_str = input("Please enter a string that needs to be encrypted: \n") 
	My_base64_encode(input_str)            
  


