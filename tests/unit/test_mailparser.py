import os
import glob
from src.emailParser import parse_email
from src.emailParser import parse_email_parts

mock_dir = '/home/developer/neo-postfix-processor/tests/mockdata'
mail_file = mock_dir + '/mail.samp'
med_sample_dir = mock_dir + '/med-samp-mail'

def read_file_off_disk(mail_sample_path):
	with open(mail_sample_path) as emailfile:
		data = emailfile.read()
	return data

def get_list_files(dirpath, pattern='*.txt'):
	if dirpath.endswith( os.path.sep) == False:
		dirpath += os.path.sep
	return glob.glob("{}{}".format(dirpath, pattern))

def test_mockmail():
	data = read_file_off_disk(mail_file)
	
	assert len(data) == 1672 

def test_readmail():
	data = read_file_off_disk(mail_file)
	assert len(data) == 1672
	actual = parse_email(data)
	text_type = actual.get_payload()[0].get_content_type()
	html_type = actual.get_payload()[1].get_content_type()
	assert text_type == 'text/plain'
	assert html_type == 'text/html'
	text = actual.get_payload()[0].get_payload()
	assert len(text) == 501

def test_read_text_off_1_mail_file():
	data = read_file_off_disk(mail_file)
	assert len(data) == 1672
	actual = parse_email_parts(data)
	assert len(actual['body_text']) == 501
	#** Confirm your subscription to the NI mate newsletter
	assert actual['body_text'][:54] == '** Confirm your subscription to the NI mate newsletter'


def test_get_med_samp_mails():
	mail_samples_list = get_list_files(med_sample_dir)
	assert len(mail_samples_list) == 33
	for mail_path in mail_samples_list:
		email_text = read_file_off_disk(mail_path)
		email_text_parts = parse_email_parts(email_text)

	
		assert type(email_text_parts) is dict	



def test_get_mail_paths():
	actual = get_list_files(med_sample_dir)
	assert type(actual) is list
	assert len(actual) == 33


