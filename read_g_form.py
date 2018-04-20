import csv
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date, timedelta
from convertdate import hebrew
import pulp

heads = ['timestamp','email','childname','dob','hschool','school','pref_main','pref_family','pref_torah','over200','holiday_dates','nondate1','nondate2','nondate3','nondate4','sameday_party','twin','accommodations','more_info']
nondatekeys=['nondate1','nondate2','nondate3','nondate4']
# NISAN = 1
# IYYAR = 2
# SIVAN = 3
# TAMMUZ = 4
# AV = 5
# ELUL = 6
# TISHRI = 7
# HESHVAN = 8
# KISLEV = 9
# TEVETH = 10
# SHEVAT = 11
# ADAR = 12
# VEADAR = 13
hmonths = ['NISAN','IYYAR','SIVAN','TAMMUZ','AV','ELUL','TISHRI','HESHVAN','KISLEV','TEVETH','SHEVAT','ADAR','VEADAR']
weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']


early_threshold = 0 # number weeks before birthday allowed
late_threshold = 10 # number of weeks after birthday at which mitzvah is not allowed
venues = 3
venue_max = 2 # max number of mitzvahs per venue per day
venue_max = [2,1,1] #main, family minyan, torah in the round

def pprint(list_of_dicts):
	print("\n\n\n")
	for d in list_of_dicts:
		print(", ".join(["{} : {}".format(k,v) for k, v in d.items()]))
		print()
	print("\n\n\n")


def readfile(filename):
	filein = open(filename, 'r')
	reader = csv.reader(filein)
	headers = next(reader, None)
	users = [{headers[i] : row[i] for i in range(len(headers)) if ((row[i] is not None) and (row[i] is not ''))} for row in reader]
	filein.seek(0)
	next(reader, None)
	xheads=['xx','holiday1','holiday2','holiday3','holiday4','holiday5','holiday6','holiday7']
	cleanusers = [{heads[i] : row[i] for i in range(len(heads)) if heads[i] not in xheads} for row in reader]
	return users, headers,cleanusers


def plus_thirteen(greg):
	(hy,hm,hd)= hebrew.from_gregorian(greg.year,greg.month,greg.day)
	if hebrew.year_months(hy+13) >= hm:
		if  hebrew.month_days(hy+13,hm) >= hd:
			#month and day fit
			hdate = (hy+13,hm,hd)
		elif hebrew.year_months(hy+13) >= hm + 1:
			#not enough days in month
			hdate = (hy + 13,hm+1,1)
		else:
			#not enough days in month, last month
			hdate = (hy + 14, 1,1)
	else:
		#not enough months in year
		hdate = (hy+14,1,1)
	return hdate

#Monday is 0, Saturday is 5, Sunday is 6
def dt_next_sat(dt):
	return dt + relativedelta(days = ((5 - dt.weekday()) % 7))

def next_sat(year,month,day):
	dt = date(year,month,day)
	dt = dt + relativedelta(days = ((5-dt.weekday()) % 7))
	return unpack(dt)

def stringify_hdate(hdate):
	return f'{hdate[2]} {hmonths[hdate[1]-1]}, {hdate[0]}'

def unpack(dt):
	return (dt.year,dt.month,dt.day)


def parse_pref(pref):
	if (pref == None) or (pref == ""):
		return 1
	for rating in range(0,5):
		if str(rating) in pref:
			return rating

today = datetime.datetime.today().date()
sat = dt_next_sat(today)

# plan['arrivalTime'] = (eventDateTime + relativedelta(minutes=arrivalMins)).isoformat()
infile = 'Google_Submissions/Mitzvah Scheduling.csv'
# constraints = readfile('constraints.csv')
people_raw, headers,people = readfile(infile)


for person in people:
	# bnei_bday = parse(person['DOB']).date() + relativedelta(years=12 if person.get('Gender')=='f' else 13)
	dob = parse(person['dob']).date()
	if dob.year == 2018:
		dob = dob.replace(year=2008)
	hdob= hebrew.from_gregorian(*unpack(dob)) #year,month,day (hebrew)
	hbmbd = plus_thirteen(dob)
	gbmbd = hebrew.to_gregorian(*hbmbd)
	bmdate = next_sat(*gbmbd)
	hbmdate = hebrew.from_gregorian(*bmdate)
	weeks_til = (date(*bmdate) - sat).days // 7
	earliest = max(0,weeks_til - early_threshold)
	latest = weeks_til + late_threshold
	nondates = []
	notes = ''
	for key in nondatekeys:
		if (person[key] is not None) and (person[key] != ''):
			nd=parse(person[key]).date()
			if nd.year==21:
				nd = nd.replace(year=2021)
			if nd.weekday() != 5:
				#if Friday or Saturday, consider as adjacent Saturday. Otherwise, exclude both adjacent Saturdays.
				if (nd.weekday() == 6):
					notes += f" Added Saturday before {nd.strftime('%A, %B %d, %Y')} to nondates."
					# nd = dt_next_sat(nd) - timedelta(days=7)
					nd = nd - timedelta(days=1)
					# nondates.append(((nd - sat).days // 7) - 1)#previous week - check this as correct behavior!
				elif (nd.weekday() == 4):
					notes += f" Added Saturday after {nd.strftime('%A, %B %d, %Y')} to nondates."
					nd = nd + timedelta(days=1)
				else:
					notes += f" Added Saturdays before & after {nd.strftime('%A, %B %d, %Y')} to nondates."
					nd = dt_next_sat(nd)
					nondates.append(((nd - sat).days // 7) - 1)
			nondates.append((nd - sat).days // 7)
			mnths = (nd.year - dob.year) * 12 + nd.month - dob.month
			if abs(mnths - 13*12) > 2:
				nondates.append((nd.replace(year=dob.year + 13) - sat).days // 7)
				notes += f" Added year before/after {nd.strftime('%A, %B %d, %Y')} to nondates."
			#check if it's a saturday. date.weekday() => Monday is 0, Sunday is 6
			#check if it's 13 years after birthday
			person[key] = parse(person[key]).date().strftime("%A, %B %d, %Y")
	holidates = person['holiday_dates'].split(';')
	if holidates == ['']:
		holidates = []
	for s in holidates:
		print(s)
		print(s.split(" - "))
		print(person['childname'])
		d1 = parse(s.split(' - ')[0],fuzzy=True,default=datetime.datetime.now().replace(year=2021)).date()
		d2 = parse(s.split(' - ')[0],fuzzy=True,default=datetime.datetime.now().replace(year=2020)).date()
		d3 = parse(s.split(' - ')[0],fuzzy=True,default=datetime.datetime.now().replace(year=2022)).date()
		for d in [d1,d2,d3]:
			if d.weekday() != 5:
				if d.weekday == 6:
					d = d-timedelta(days=1)
				else:
					d= dt_next_sat(d)
			nondates.append((d-sat).days // 7)
	person['hDOB']= hdob
	person['dob']=dob
	person['hbmbd']=hbmbd
	person['gbmbd']=gbmbd
	person['bmdate']=bmdate
	person['hbmdate']= hbmdate
	person['hfullbd'] = stringify_hdate(hdob)
	person['hfullbmbd'] = stringify_hdate(hbmbd)
	person['hfullbmdate']=stringify_hdate(hbmdate)
	person['weeks_til']= weeks_til
	person['earliest'] = earliest
	person['latest'] = latest
	person['nondates'] = nondates
	person['notes']=notes
datestuff = ['dob','hfullbd','bmdate','hfullbmdate']
pprint([{key:person[key] for key in datestuff} for person in people])
# pprint([{key:val for key,val in person.items() if key in datestuff} for person in people])
schools = sorted(list({person.get('school') for person in people}))
dates = sorted(list({d for person in people for d in range(person['earliest'],person['latest']+1)}))


date_inds = {date : i for i, date in enumerate(dates)}
for person in people:
	person['bday_index'] = date_inds[person['weeks_til']]
	person['earliest_index'] = date_inds[person['earliest']]
	person['latest_index'] = date_inds[person['latest']]
	person['school_id'] = schools.index(person['school'])
	person['nondate_inds'] = [date_inds[d] for d in person['nondates'] if (date_inds.get(d) is not None)] #ignore nondate if outside range of potential dates

# # school_date_conflicts[(school_id,d)]=[i1,i2,i3,...] contains a list of all indices of students eligible for mitzvah on day d who attend school school_id. All such lists are of length at least 2, otherwise no conflict.
# # date_prospects[d] contains a list of tuples (i,l) where for person indices i and school_id l if person i is eligible for mitzvah on date d
school_date_conflicts = {}
date_prospects = [[] for d in dates]
for i,person in enumerate(people):
	for d in range(person['earliest_index'],person['latest_index']):
		if any([other[1]==person['school_id'] for other in date_prospects[d]]):
			school_date_conflicts[(person['school_id'],d)] = [i] + [other[0] for other in date_prospects[d] if other[1] == person['school_id']]
		date_prospects[d].append((i,person['school_id']))

venue_keys = ['pref_main','pref_family','pref_torah']
#venue ratings
for person in people:
	for preflabel in venue_keys:
		person[preflabel] = parse_pref(person[preflabel])
pref_vector = []

n = sum(((person['latest_index'] - person['earliest_index'])*venues for person in people)) # x_i_j_k is person i at venue j, date k
print("Number of decision variables: " + str(n))

x=pulp.LpVariable.dicts('assignments',range(0,n),lowBound=0,upBound=1,cat=pulp.LpBinary)
m=pulp.LpVariable.dicts('school-date-limits',range(0,len(school_date_conflicts)*venues),lowBound=0,upBound=1,cat=pulp.LpBinary)
assignment_model=pulp.LpProblem('assignment model',pulp.LpMinimize)

I = {}
Ix = []
ind = 0
# forall i, Sum_j,k x_i_j_k == 1
# x[I[(i,j,k)]] = x_i_j_k
# Ix[I[(i,j,k)]] = (i,j,k)
for i,person in enumerate(people):
	ensure_mitzvah=[]
	for j in range(venues):
		for k in range(person['earliest_index'],person['latest_index']):
			I[(i,j,k)] = ind
			Ix.append((i,j,k))
			ensure_mitzvah.append(1*x[ind])
			pref_vector.append((-1*person[venue_keys[j]])*x[ind]) #venue preferences
			#set nondates equal to zero
			if k in person['nondate_inds']:
				# assignment_model += pulp.lpSum([1*x[ind]]) == 0
				assignment_model += x[ind]==0
			ind +=1
	assignment_model += pulp.lpSum(ensure_mitzvah)==1

# # Add penalty for bnei mitzvah being n weeks after birthday.
# #OPTIONAL: minimize number of venues in use per weekend? is there "pulp.lpMax" for m[ind] variables?
penalty_per_week = 1
lateness_penalties = [penalty_per_week*(abs(dates[k]-people[i]['weeks_til']))*x[ind] for ind, (i,j,k) in enumerate(Ix)]

#Restrict nondates:
#TODO
assignment_model += pulp.lpSum(lateness_penalties + pref_vector) #add to objective function


Im = {}
Imx = []
ind = 0
for r, ((l,k),students) in enumerate(school_date_conflicts.items()):
	onevenue = []
	for j in range(venues):
		Im[(j,l,k)] = ind
		Imx.append((j,l,k))
		onevenue.append(1*m[ind])
		for i in students:
			assignment_model += pulp.lpSum([1*x[I[(i,j,k)]],-1*m[ind]]) <= 0
		ind +=1
	assignment_model += pulp.lpSum(onevenue)<=1

# # Venue j can host at maximum venue_max[j] mitzvahs in a day
for k,date_student_school_tuples in enumerate(date_prospects):
	for j in range(venues):
		if len(date_student_school_tuples) > venue_max[j]:
			venuelimit = []
			for (i,l) in date_student_school_tuples:
				venuelimit.append(1*x[I[(i,j,k)]])
			assignment_model += pulp.lpSum(venuelimit) <= venue_max[j]



assignment_model.solve()
x =[val.varValue for k,val in x.items()]

ones = [i for i, v in enumerate(x) if v == 1]
winners = [Ix[v] for v in ones]

for (i,j,k) in winners:
	people[i]['venue'] = j
	people[i]['best_week'] = dates[k]

for person in people:
	person['earliest'] = (sat + relativedelta(weeks=person['earliest'])).strftime("%A, %B %d, %Y")
	person['latest'] = (sat + relativedelta(weeks=person['latest'])).strftime("%A, %B %d, %Y")
	person['best_week'] = (sat + relativedelta(weeks=person['best_week'])).strftime("%B %d, %Y")
	for key in ['earliest_index','latest_index','bday_index','school_id','earliest','latest','hDOB','hbmbd',
	'gbmbd','bmdate','hbmdate']:
		del person[key]

outfilename = infile.split('.')
outfilename[-2] +='_solution'
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=[k for k in people[0]])
	writer.writeheader()
	for person in people:
		writer.writerow(person)

optheads = ['dob','school','pref_main','pref_family','pref_torah','holiday_dates','nondate1','nondate2','nondate3','nondate4','accommodations','more_info','nondates','notes','venue','best_week']
outfilename = infile.split('.')
outfilename[-2] +='_solution_basic'
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=optheads)
	writer.writeheader()
	for person in people:
		writer.writerow({key:person[key] for key in optheads})
pprint(people)

## TODO:
# Venue rankings - DONE
# Date restrictions - DONE
# holiday_dates
# older students (within same week) getting preference
# some nondates given with wrong year - change?
# if a nondate is not a saturday -- ??
