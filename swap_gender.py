""" Code to produce a gender swapped english sentence. This is a brute force
implementation that requires the specification of gender pairs.
Inspired by https://www.geeksforgeeks.org/change-gender-given-string/ """

def swap_genders(gender_sentence_filename,out_filename):

	gender_pairs = \
	{'he':'she', 'she':'he',\
	'him':'her','her':'him',\
	'his':'her','her':'his',\
	'boy':'girl','girl':'boy',\
	'father':'mother','mother':'father',\
	'husband':'wife','wife':'husband',\
	'male':'female','female':'male',\
	'man':'woman','woman':'man',\
	'mr.':'ms.','ms.':'mr.',\
	'sir':'madam','madam':'sir',\
	'son':'daughter','daughter':'son',\
	'uncle':'aunt','aunt':'uncle'}

	with open(gender_sentence_filename) as org_file, open(out_filename,'w') as swapped_file:

		for line in org_file:
			words = line.strip().split(' ')
			case = [1 if ((word[0].isupper()) or (word[0] == "\"" \
				and len(word) > 1 and word[1].isupper())) else 0 for word in words]
			words = [word.lower() for word in words]
			out_words = [gender_pairs[word] if word in gender_pairs else word for word in words]
			out_words = [word.title() if case[i] else word for (i,word) in enumerate(out_words)]
			out_sentence = ' '.join(word for word in out_words)

			swapped_file.write(line)
			swapped_file.write(out_sentence+'\n\n')


# in_file = "../gen_files/en_genders.txt"
# out_file = "../gen_files/en_gen_swap.txt"

# swap_genders(in_file,out_file)