#_*_coding:utf-8_*_

def generate_hotmap_data(candidate_mode):
	filename = 'Data/' + candidate_mode + '_count.csv' 
	candidate_count = []

	with open(filename) as file:
		for line in file:
			line = line.strip().split(',')
			state_code,count = line[0],line[1]
			candidate_count.append(count)

	return candidate_count

def sentiment_compare_mode(candidate_mode):
	positive_filename = 'Data/' + candidate_mode + '_positive' + '_count.csv'
	negative_filename = 'Data/' + candidate_mode + '_negative' + '_count.csv'
	positive_candidate_count = []
	negative_candidate_count = []
	result_candidate_count = []

	with open(positive_filename) as file:
		for line in file:
			line = line.strip().split(',')
			state_code,count = line[0],line[1]
			positive_candidate_count.append(count)

	with open(negative_filename) as file:
		for line in file:
			line = line.strip().split(',')
			state_code,count = line[0],line[1]
			negative_candidate_count.append(count)

	for i in range(len(positive_candidate_count)):
		if positive_candidate_count[i] >= negative_candidate_count[i]:
			result_candidate_count.append(1)
		
		else:
			result_candidate_count.append(-1)

	return result_candidate_count

def candidate_comparison(comparison_mode,time_period):
	biden_popularity_filename = 'Data/' + time_period + '_biden' + '_count.csv'
	biden_positive_filename = 'Data/' + time_period + '_biden' + '_positive' + '_count.csv'
	biden_negative_filename = 'Data/' + time_period + '_biden' + '_negative' + '_count.csv'
	trump_popularity_filename = 'Data/' + time_period + '_trump' + '_count.csv'
	trump_positive_filename = 'Data/' + time_period + '_trump' + '_positive' + '_count.csv'
	trump_negative_filename = 'Data/' + time_period + '_trump' + '_negative' + '_count.csv'
	biden_count = []
	biden_positive_count = []
	biden_negative_count = []
	trump_count = []
	trump_positive_count = []
	trump_negative_count = []
	result_count = []

	if comparison_mode == 'popularity':
		with open(biden_popularity_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				biden_count.append(count)

		with open(trump_popularity_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				trump_count.append(count)

		for i in range(len(biden_count)):
			if biden_count[i] >= trump_count[i]:
				result_count.append(1)
		
			else:
				result_count.append(0)

	elif comparison_mode == 'positive':
		with open(biden_positive_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				biden_positive_count.append(count)

		with open(trump_positive_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				trump_positive_count.append(count)

		for i in range(len(biden_positive_count)):
			if biden_positive_count[i] >= trump_positive_count[i]:
				result_count.append(1)
		
			else:
				result_count.append(0)

	elif comparison_mode == 'negative':
		with open(biden_negative_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				biden_negative_count.append(count)

		with open(trump_negative_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				trump_negative_count.append(count)

		for i in range(len(biden_negative_count)):
			if biden_negative_count[i] >= trump_negative_count[i]:
				result_count.append(1)
		
			else:
				result_count.append(0)

	else:
		with open(biden_positive_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				biden_positive_count.append(count)

		with open(trump_positive_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				trump_positive_count.append(count)

		with open(biden_negative_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				biden_negative_count.append(count)

		with open(trump_negative_filename) as file:
			for line in file:
				line = line.strip().split(',')
				state_code,count = line[0],line[1]
				trump_negative_count.append(count)

		if comparison_mode == 'tendency':
			for i in range(len(biden_positive_count)):
				val = (int(biden_positive_count[i]) + int(trump_negative_count[i])) - (int(biden_negative_count[i]) + int(trump_positive_count[i]))
				result_count.append(val)
		else:
			for i in range(len(biden_positive_count)):
				val = (int(biden_positive_count[i]) + int(trump_negative_count[i])) - (int(biden_negative_count[i]) + int(trump_positive_count[i]))
				
				if val >= 0:
					result_count.append(1)
				else:
					result_count.append(0)

	return result_count


def compute_voter(comparison_mode,time_period):
	biden = 0
	trump = 0
	result_count = candidate_comparison(comparison_mode,time_period)
	voter = [3,9,6,11,55,9,7,3,3,29,16,4,4,20,11,6,4,8,8,4,10,11,16,10,6,10,3,5,6,4,14,5,29,15,3,18,7,7,20,2,4,9,3,11,38,6,3,13,12,5,10,3]

	for i in range(len(result_count)): 
		if result_count[i] == 1: #Biden
			biden = biden + voter[i]
		else:
			trump = trump + voter[i]

	return biden,trump





