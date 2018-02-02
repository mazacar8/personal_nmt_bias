# Class that includes functions to pre process training data for gender
# specific requirements. Training data is for translations from a gender
# neutral language to English.
# swapGender inspired by https://www.geeksforgeeks.org/change-gender-given-string/

import argparse

class GenderPreProcess:

	def __init__(self,en_file,lang2_file):

		self.en_file = en_file
		self.l2_file = lang2_file

		self.male_search_words = ['he ']

		self.female_search_words = ['she ']

		self.gender_pairs = \
		{'he':'she', 'she':'he'}

		# self.male_search_words = ['he ','him ','his ', 'boy ', 'father ', \
		# 'husband ', 'male ','man ','mr. ','sir ','son ','uncle ', 'men\'s ']

		# self.female_search_words = ['she ','her ', 'girl ','mother ','wife ',\
		#  'female ','woman ', 'ms. ','madam ','daughter ','aunt ', 'women\'s ']

		#Still need to add swaps for 2nd language.
		# self.gender_pairs = \
		# {'he':'she', 'she':'he',\
		# 'him':'her','her':'him',\
		# 'his':'her','her':'his',\
		# 'boy':'girl','girl':'boy',\
		# 'father':'mother','mother':'father',\
		# 'husband':'wife','wife':'husband',\
		# 'male':'female','female':'male',\
		# 'man':'woman','woman':'man',\
		# 'mr.':'ms.','ms.':'mr.',\
		# 'sir':'madam','madam':'sir',\
		# 'son':'daughter','daughter':'son',\
		# 'uncle':'aunt','aunt':'uncle',\
		# 'men\'s':'women\'s','women\'s':'men\'s '}

	#Determines if a given sentence has any indication of the male gender
	def maleIndicated(self,line):
		lc_line = line.strip().lower()
		for w in self.male_search_words:
			spaced = " "+w
			if (lc_line[0:len(w)] == w) or (spaced in lc_line):
				return True
		return False

	#Determines if a given sentence has any indication of the female gender
	def femaleIndicated(self,line):
		lc_line = line.strip().lower()
		for w in self.female_search_words:
			spaced = " "+w
			if (lc_line[0:len(w)] == w) or (spaced in lc_line):
				return True
		return False

	#Swaps all gender specific words in a given sentence
	#Inspired by https://www.geeksforgeeks.org/change-gender-given-string/
	def swapGender(self,line):
		words = line.strip().split(' ')
		case = [1 if ((word[0].isupper()) or (word[0] == "\"" \
			and len(word) > 1 and word[1].isupper())) else 0 for word in words]
		words = [word.lower() for word in words]
		out_words = [self.gender_pairs[word] if word in self.gender_pairs \
		else word for word in words]
		out_words = [word.title() if case[i] else word for (i,word) in \
		enumerate(out_words)]
		out_sentence = ' '.join(word for word in out_words)

		return out_sentence+'\n'

	#Creates a file with the name specified in new_train_file which includes
	#gender swapped instances of the training set. Also prints out gender
	#related counts and optionally creates male/female files 
	def addGenderExceptions(self,new_train_file_en,new_train_file_l2,\
		male_file,female_file):

		num_male = 0
		num_female = 0
		num_both = 0
		num_gender = 0

		#Optional creation of male/female specific files
		if male_file != None:
			male_f = open(male_file,'w')
		if female_file != None:
			female_f = open(female_file,'w')

		with open(self.en_file) as en_file, \
		open(self.l2_file) as l2_file,\
		open(new_train_file_en,'w') as new_file_en,\
		open(new_train_file_l2,'w') as new_file_l2 :

			for line in en_file:

				l2_line = l2_file.readline()

				male = self.maleIndicated(line)
				female = self.femaleIndicated(line)
				genderIndicated = male or female

				if genderIndicated:
					swapped_line = self.swapGender(line)
					new_file_en.write(line+swapped_line)
					new_file_l2.write(l2_line+l2_line)
					num_gender += 1

				else:
					new_file_en.write(line)
					new_file_l2.write(l2_line)

				#Optional creation of male/female specific files
				if male_file != None and male:
					male_f.write(line)

				if female_file != None and female:
					female_f.write(line)

				num_male += 1 if male else 0
				num_female += 1 if female else 0
				num_both += 1 if male and female else 0

		if male_file != None:
			male_f.close()
		if female_file != None:
			female_f.close()

		print """Total Gender Indications = %d\nMale Indications = %d
Female Indications = %d\nBoth Genders = %d"""%(num_gender,num_male,num_female,num_both)

def main():

	parser = argparse.ArgumentParser(description=\
		"Add English gender exceptions to Training Data")

	parser.add_argument('en_file', metavar='infile1', type=str, \
		help='File containg English version of sentences')
	parser.add_argument('l2_file', metavar='infile2', type=str, \
		help='File containg corresponding sentences for gender neutral language')

	parser.add_argument('new_en_file', metavar='outfile1', type=str, \
	help='Output file with the addition of gender swap exceptions')

	parser.add_argument('new_l2_file', metavar='outfile2', type=str, \
	help='Output file with the addition of gender neutral duplicates')

	parser.add_argument('--en_male_file', dest='male_outfile', type=str, \
	default = None,\
	help='Optional output file containing sentences with male indicators')

	parser.add_argument('--en_female_file', dest='female_outfile', type=str, \
	default = None,\
	help='Optional output file containing sentences with female indicators')
	
	args = parser.parse_args()
	gpp = GenderPreProcess(args.en_file,args.l2_file)
	gpp.addGenderExceptions(args.new_en_file,args.new_l2_file,\
		args.male_outfile,args.female_outfile)

if __name__ == "__main__":
	main()



