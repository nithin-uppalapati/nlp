# A Space efficient Dynamic Programming
# based Python3 program to find minimum
# number operations to convert str1 to str2
def EditDistDP(str1, str2):
	
	len1 = len(str1)
	len2 = len(str2)

	# Create a DP array to memoize result
	# of previous computations
	DP = [[0 for i in range(len1 + 1)]
			for j in range(2)];

	# Base condition when second String
	# is empty then we remove all characters
	for i in range(0, len1 + 1):
		DP[0][i] = i

	# Start filling the DP
	# This loop run for every
	# character in second String
	for i in range(1, len2 + 1):
		
		# This loop compares the char from
		# second String with first String
		# characters
		for j in range(0, len1 + 1):

			# If first String is empty then
			# we have to perform add character
			# operation to get second String
			if (j == 0):
				DP[i % 2][j] = i

			# If character from both String
			# is same then we do not perform any
			# operation . here i % 2 is for bound
			# the row number.
			elif(str1[j - 1] == str2[i-1]):
				DP[i % 2][j] = DP[(i - 1) % 2][j - 1]
			
			# If character from both String is
			# not same then we take the minimum
			# from three specified operation
			else:
				DP[i % 2][j] = (1 + min(DP[(i - 1) % 2][j],
									min(DP[i % 2][j - 1],
								DP[(i - 1) % 2][j - 1])))
			
	# After complete fill the DP array
	# if the len2 is even then we end
	# up in the 0th row else we end up
	# in the 1th row so we take len2 % 2
	# to get row
	sol=DP[len2 % 2][len1]
	print(sol)

# Driver code
if __name__ == '__main__':
	
	str1 = "food"
	str2 = "money"
	
	EditDistDP(str1, str2)

# This code is contributed by gauravrajput1

