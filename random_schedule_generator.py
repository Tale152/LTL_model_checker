# 
# In case you want to run some tests on several paths,
# here is a random path generator:
# 


import random

def coin():
	return (random.getrandbits(1) == 1)


def make_schedule(file,items = ['wolf','cabbage','goat','spinach','popeye','computer','wine'],length = 1000,loop = 420):
	lasso = length - loop
	sched = {}
	side = {}
	emp = 'employee'
	l = '_left'
	r = '_right'
	t = '_trans'
	n = ' '
	lassosit = [ [] for thing in items]
	sched[emp] = []
	for i in range(4*length+4):
		mv = coin()
		sched[emp].append(mv)
	if sched[emp][0]:
		side[emp] = [l]
	else:
		side[emp] = [r]
	emp_now = side[emp][0]
	emp_before = n
	for change in sched[emp]:
		if change:
			side[emp].append(t)
			if emp_now == l:
				side[emp].append(r)
				emp_now = r
			else: 
				side[emp].append(l)
				emp_now = l
		else:
			side[emp].append(side[emp][-1])
		# elif emp_now == t:
		# 	if emp_before == l:
		# 		emp_before = emp_now
		# 		emp_now = r
		# side[emp].append(emp_now)
	# for corrections... ??
	while not (side[emp][lasso] == r):
		lasso += 1
		length += 1
	length += 4
	
# Corrections:

	side[emp] = side[emp][:length-4]
	if side[emp][-1] == t:
		side[emp] = side[emp][:length-5]
		length -=1
		lasso-=1
	correctioncase = ''

	with open(file,'w') as out:
		out.write(str(length) + ' ' + str(loop))
	
	if side[emp][-1] == l:
		side[emp].append(l)
		side[emp].append(t)
		side[emp].append(r)
		side[emp].append(r)
		correctioncase = 'ltrr'
	elif side[emp][-1] == r:
		side[emp].append(t)
		side[emp].append(l)
		side[emp].append(t)
		side[emp].append(r)
		correctioncase = 'tltr'
	elif side[emp][-1] == t:
		if side[emp][-2] == l:
			side[emp].append(r)
			side[emp].append(t)
			side[emp].append(l)
			side[emp].append(t)
			correctioncase = 'rtlt'
		elif side[emp][-2] == r:
			side[emp].append(l)
			side[emp].append(t)
			side[emp].append(r)
			side[emp].append(r)
			correctioncase = 'ltrr'

	for thing in items:
		sched[thing] = []
		for i in range(length):
			ap = coin()
			mv = coin()
			sched[thing].append((mv,ap))

	start_l = [ (sched[thing][0][0] and sched[thing][0][1]) for thing in items ]
	start_r = [ (sched[thing][0][0] and not sched[thing][0][1]) for thing in items ]
	start_t = [ False for thing in items ]
	for i in range(len(items)):
		temp_l = [start_l[i]]
		temp_r = [start_r[i]]
		temp_t = [start_t[i]]
		for count in range(length -4)[1:]:
			app, move = sched[items[i]][count]
			exists = temp_l[-1] or temp_r[-1] or temp_t[-1]
			intran = temp_t[-1]
			atleft = temp_l[-1]
			atright = temp_r[-1]
			move = (move and (side[emp][count] == t))
			if not exists:
				temp_l.append(app)
				temp_r.append(False)
				temp_t.append(False)
			elif atright and app:
				temp_l.append(False)
				temp_r.append(False)
				temp_t.append(False)
			elif not intran and move:
				temp_l.append(False)
				temp_t.append(True)
				temp_r.append(False)
			elif not intran:
				temp_l.append(atleft)
				temp_t.append(intran)
				temp_r.append(atright)
			elif intran:
				befl = temp_l[-2]
				befr = temp_r[-2]
				temp_l.append(befr)
				temp_t.append(False)
				temp_r.append(befl)
			else:
				print('something went wrong')
			if count == lasso:
				lassosit[i] = [temp_l[-1],temp_t[-1],temp_r[-1]]


		exists = temp_l[-1] or temp_r[-1] or temp_t[-1]
		intran = temp_t[-1]
		atleft = temp_l[-1]
		atright = temp_r[-1]
		exlasso = temp_l[lasso] or temp_r[lasso] or temp_t[lasso]
		latran = temp_t[lasso]
		laleft = temp_l[lasso]
		laright = temp_r[lasso]
		

		if laleft and not exists:
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
		elif (not exlasso) and (atright or not exists):
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
		elif laleft and atleft:
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
		elif laright and atright:
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
		elif laleft and atright:
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
		elif correctioncase == 'ltrr':
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(True)
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
		elif correctioncase == 'tltr':
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(True)
			temp_l.append(False)
			temp_r.append(True)
			temp_t.append(False)
		elif correctioncase == 'rtlt':
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(True)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(True)
		else:	
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)
			temp_l.append(False)
			temp_r.append(False)
			temp_t.append(False)

		where = []
		for count in range(length):
			if temp_l[count]:
				where.append(l)
			elif temp_r[count]:
				where.append(r)
			elif temp_t[count]:
				where.append(t)
			else:
				where.append(n)
		side[items[i]] = where
	with open(file,'a') as out:
		for i in range(length):
			out.write('\n')
			for thing in items:
				if not (side[thing][i] == n):
					out.write(thing + side[thing][i] + ' ')
			out.write(emp + side[emp][i])



