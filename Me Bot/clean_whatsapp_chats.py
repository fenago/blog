import pickle
import random
import sys
import os

YOUR_NAME = 'YOUR_NAME'
OTHER_NAME = 'OTHER_NAME'

def read_file():
	chat_file = sys.argv[1]
	f = open(chat_file,'r', encoding="utf8")
	content = f.readlines()
	return content


def extract_text(content):
	all_text = []
	your_sents = []
	other_sents = []

	prev_pr_to_sp = {}
	prev = None
	for line in content[1:]:
		if 'Missed Voice Call' in line:
			continue
		if 'image omitted' in line:
			continue
		if '{}: '.format(YOUR_NAME) in line:
			text = line.split('{}: '.format(YOUR_NAME))[-1]
			your_sents.append(text)
			all_text.append(text)
			if prev == 'None':
				continue
			if prev == 'pr':
				prev_pr_to_sp[other_sents[-1]] = text
			prev = 'sp'
		elif '{}: '.format(OTHER_NAME) in line:
			text = line.split('{}: '.format(OTHER_NAME))[-1]
			other_sents.append(text)
			all_text.append(text)
			prev = 'pr'
		else:
		
			all_text[-1] += line

			if prev == 'sp':
				your_sents[-1] += line
			elif prev == 'pr':
				other_sents[-1] += line
	
	return all_text, your_sents, other_sents, prev_pr_to_sp

def make_directory():
	if not os.path.isdir('texts/whatsapp'):
		if not os.path.isdir('texts'):
			os.mkdir('texts')
		os.mkdir('texts/whatsapp')


def write_to_files(file_name, texts):
	f = open(file_name, 'wb')
	pickle.dump(texts, f)
	f.close()


	
content = read_file()
all_text, your_sents, other_sents, prev_pr_to_sp = extract_text(content)
make_directory()
write_to_files('texts/whatsapp/dilogues.p', prev_pr_to_sp)
write_to_files('texts/whatsapp/all_text.p', all_text)
write_to_files('texts/whatsapp/your_sents.p', your_sents)
write_to_files('texts/whatsapp/other_sents.p', other_sents)


