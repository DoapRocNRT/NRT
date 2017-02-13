import os

def setStart(strng):
	strng = strng.split()[-1]
	start_val = ''
	for char in strng: 
		if char.isdigit() == True:
			start_val = start_val + char
		if char == '_': 
			break
	return int(start_val)

def setEnd(strng): 
	strng = strng.split()[-1]
	end_val = ''
	strng = strng.split('_')[1]
	for char in strng:
		if char.isdigit()==True: 
			end_val = end_val + char
		if char.isdigit()==False: 
			break
	return int(end_val)

def getTimes_eachline(transcript_lines):
	all_times = []
	l = 0
	for line in transcript_lines:
		if '*' in line[0:1]:
			n = l
			while True: 
				try: 
					start_time =  setStart(transcript_lines[n])
					end_time = setEnd(transcript_lines[n])
					tup = (start_time, end_time)
					all_times.append(tup)
					break
				except (ValueError, IndexError):
					n = n + 1
		l = l+1
	return all_times

def getTimes(transcript_filename):
	transcript = open(transcript_filename).read()
	transcript_lines = transcript.splitlines()

	check = [0, 0, 0, 0]
	which_line = [0,0,0,0]
	all_times_c = []
	all_times_s = []
	i = 0

	for line in transcript_lines: 
		if '@' in line[0:3]: 	
			if ('@G:') in line and ('Cinderella' in line) and ('Cinderella_Intro' not in line) and ('Cinderella_intro' not in line):
				z = i+1   
				while '%' not in transcript_lines[z][0]:
					z=z+1
				
				start_val_c = setStart(transcript_lines[z-1]) 	#START TIME OF CINDERLLA 
				check[0] = start_val_c; 						#stored cinderella start time
				start_i_c = z+2									#stored which_line 
				
			elif (check[0] != 0) & (check[1] == 0): 
				n = i;
				while ('*' not in transcript_lines[n][0]) or ('www' in transcript_lines[n]):
					n = n-1
				while True: 
					try: 
						end_val_c = setEnd(transcript_lines[n]) #END TIME OF CINDERELLA 
						break
					except IndexError:
						n = n + 1
				check[1] = end_val_c 									#store cinderella end time here
				end_i_c = n-1	

				if start_i_c != 0:										#end which_line 
					all_times_c = getTimes_eachline(transcript_lines[start_i_c:end_i_c])  #get other time stamps 

			if ('Sandwich' in line) and ('Sandwich_Intro' not in line):
				z = i + 1
				print line, transcript_filename
				while '%' not in transcript_lines[z][0]:
					z=z+1
				start_val_s = setStart(transcript_lines[z-1]) #START TIME OF SANDWHICH
				check[2] = start_val_s;						  #store start time 
				start_i_s = z+1 								  #which_line start


				while '@' not in transcript_lines[z][0]:
					z = z+1   #finds the end 
				while ('*' not in transcript_lines[z][0]) or ('www' in transcript_lines[z]):
					z = z-1   #finds the part where there'd be a time stamp
				while True: 
					try: 
						end_val_s = setEnd(transcript_lines[z]) #end of sandwich task [second value]
						check[3] = end_val_s;
						break
					except IndexError:
						z = z+1 
				end_i_s = z-1

				if start_i_s != 0:
					all_times_s = getTimes_eachline(transcript_lines[start_i_s:end_i_s])
				break		
		i = i+1
	check.append(all_times_c)
	check.append(all_times_s)
	return check   #[start_val_c, end_val_c, start_val_s, end_val_s, other_lines_c, other_lines_s]
	
def write_values(dir, fn):
	fn.write('filename,start_cind,end_cind,start_sand,end_sand,other_c,other_s\n')
	aph_dir = os.chdir("Aphasia")
	dir_list = next(os.walk('.'))[1]
	for sub_dir in dir_list:
		os.chdir(sub_dir)
		for filename in os.listdir('.'):
			if filename[-5] =='a':
				times = getTimes(filename);
				s = filename 
				for t in times: 
					s = s + ',' + str(t)
				s = s + '\n'
				fn.write(s)
		os.chdir('..')

all_values_a  = open('all_values_aphasia.csv', 'w') 
all_values_c = open('all_values_control.csv', 'w')  

write_values("Aphasia", all_values_a)
os.chdir("..")
write_values("Control", all_values_c)

