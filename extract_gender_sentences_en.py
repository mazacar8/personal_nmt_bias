""" Code to extract English-Turkish training sentences where 
the English translation specifies a gender pronoun in several different formats"""

en_file_loc = '../Datasets/en-tr/SETIMES2.en-tr.en'
tr_file_loc = '../Datasets/en-tr/SETIMES2.en-tr.tr'
en_tr_male = '../gen_files/en-tr_male.txt' #File with english sentences with male indicators and turkish translation 
en_tr_female = '../gen_files/en-tr_female.txt' #File with english sentences with female indicators and turkish translation 
en_tr_genders  = '../gen_files/en-tr_genders.txt' #File with english sentences with both gender indicators and turkish translation 
en_genders  = '../gen_files/en_genders.txt' #File with only english sentences with both gender indicators
male_search_words = ['he ','him ','his ', 'boy ', 'father ', 'husband ', 'male ','man ','mr. ','sir ','son ','uncle ']
female_search_words = ['she ','her ', 'girl ','mother ','wife ', 'female ','woman ', 'ms. ','madam ','daughter ','aunt ']

with open(en_file_loc) as en_file, open(tr_file_loc) as tr_file,\
open(en_tr_male,'w') as male_file, open(en_tr_female,'w') as female_file,\
open(en_tr_genders,'w') as en_tr_genders_file, open(en_genders,'w') as en_genders_file:
	male_indicators = 0
	female_indicators = 0
	both = 0
	total = 0
	for line in en_file:
		
		tr_line = tr_file.readline()
		male_indicated = False
		female_indicated = False
		lower_case_en = line.strip().lower()

		for w in male_search_words:
			spaced = " "+w
			if (lower_case_en[0:len(w)] == w) or (spaced in lower_case_en):
				male_indicated = True
				male_indicators += 1
				male_file.write(line)
				male_file.write(tr_line+'\n')
				break

		for w in female_search_words:
			spaced = " "+w
			if (lower_case_en[0:len(w)] == w) or (spaced in lower_case_en):
				female_indicated = True
				female_indicators += 1 
				female_file.write(line)
				female_file.write(tr_line+'\n')
				break

		if male_indicated and female_indicated:

			both += 1

		if male_indicated or female_indicated:
			en_tr_genders_file.write(line)
			en_tr_genders_file.write(tr_line+'\n')
			en_genders_file.write(line)
			total += 1

	print total, male_indicators, female_indicators, both