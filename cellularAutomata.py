"""This program is a representation of cellular automata.

The program will ask for several variables and evolve a state over several steps.

"""

def cellular_automata(num_elements, num_alphabet, cellular_automata, num_steps):
	"""Takes a state and evolves it over n steps.
	
	The final output will look like:
		0001
		1001
		0101
		1111
	"""
	
	ca_next = cellular_automata[:] # List representation of next state
	
	print(*ca_next)	# Prints the starting state

	step = 1 # Number of current state

	while (step < num_steps):
		ca_next = []	# Reset list for every new step

		for i in range(0, num_elements):	# Add elements to next state according to update rule
			if i > 0:
				ca_next.append( (cellular_automata[i-1]+cellular_automata[i]) % num_alphabet)
				
			elif(i == 0):
				ca_next.append( (cellular_automata[num_elements - 1]+cellular_automata[i]) % num_alphabet)

		print (*ca_next)

		cellular_automata = ca_next[:] # Update cell list

		step += 1	# Step increment

if __name__ == '__main__':
	""" Main function will serve as the driver for the program.

	It takes user input and runs cellular_automata() with given parameters:

		num_elements	-- Number of elements in automaton
		num_alphabet	-- Number of elements in the alphabet
							-- In general, our alphabet will be numerical, starting at 0, and incrementing up to user input.
		start_state		-- Starting state of automaton
		update_rule		-- Rule that governs how the automaton will evolve
							-- In general, the rule will be of the form: ( a + b + c + ... + n ) mod m, where a...n are elements of the previous state, and m is the number of elements in the alphabet.
		num_steps		-- Number of steps through which the automaton will evolve
	"""

	num_elements = int(input ('Enter # of elements in automaton: '))

	num_alphabet = int(input ('Enter # of elements in alphabet: '))

	alphabet = [] # Used to make a nice visualization in the terminal

	for i in range(0, num_alphabet):
		alphabet.append(i)
	print('Your alphabet is', *alphabet)

	start_state = [] # Starting state will be appended one element at a time.

	print ('Enter starting state, one element per line: ')
	for i in range(0, num_elements):
		element = int(input())
		start_state.append(element)

	# update_rule = input ('Enter update rule: ')

	num_steps = int(input ('Enter # of steps the automaton will take: '))

	print ('\n\nBeginning process...\n')
	cellular_automata(num_elements, num_alphabet, start_state, num_steps)