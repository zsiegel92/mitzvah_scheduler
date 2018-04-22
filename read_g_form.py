import csv
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date, timedelta
from convertdate import hebrew
import pulp
from Google_Submissions.extra_info import extra_kw, extra#,extra_defaults


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
late_threshold = 15 # number of weeks after birthday at which mitzvah is not allowed
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
			#another month in year, not enough days in month
			if (hm+1 == 7):
				hdate = (hy + 14,hm+1,1)
			else:
				hdate = (hy + 13,hm+1,1)
		else:
			#not enough months in year, not enough days in month
			hdate = (hy + 13, 1,1)
	else:
		#not enough months in year
		hdate = (hy+13,1,1)
	return hdate

def plus_thirteen2(greg):
	(hy,hm,hd)= hebrew.from_gregorian(greg.year,greg.month,greg.day)
	h = hebrew.to_jd_gregorianyear(greg.year+13,hm,hd)
	print(f"Converted gregorian {greg} to hebrew {h}")
	return h

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

def find_by_name(name,ls):
	for el in ls:
		if (name.lower() in el['childname'].lower()) or (el['childname'].lower() in name.lower()):
			return el
	return None

def index_by_name(name,ls):
	for i,el in enumerate(ls):
		if (name.lower() in el['childname'].lower()) or (el['childname'].lower() in name.lower()):
			return i
	return None
def week_to_date(wk,this_sat):
	if wk is None:
		return "None"
	return (this_sat + relativedelta(weeks=wk)).strftime("%B %d, %Y")

def dt_to_week(dt,this_sat):
	return (dt-sat).days // 7

today = datetime.datetime.today().date()
sat = dt_next_sat(today)
summer_end_str= "Saturday, September 4, 2021"
summer_start_str = "Saturday, June 5, 2021"
summer_range = (parse(summer_start_str),parse(summer_end_str))
summer_start = dt_to_week(parse(summer_start_str).date(),sat)
summer_length = 10
summer_dates = list(range(summer_start,summer_start + summer_length + 1))
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
	weeks_til = dt_to_week(date(*bmdate),sat)
	earliest = max(0,weeks_til - early_threshold)
	latest = weeks_til + late_threshold
	days_before_sat = (date(year = bmdate[0],month=bmdate[1],day=bmdate[2]) - date(year = gbmbd[0], month = gbmbd[1],day= gbmbd[2])).days
	# print(f"bmdate is {date(year = bmdate[0],month=bmdate[1],day=bmdate[2]).strftime('%A, %B %d, %Y')}, gbmbd is {date(year = gbmbd[0], month = gbmbd[1],day= gbmbd[2]).strftime('%A, %B %d, %Y')}, and days_before_sat is {days_before_sat}\n")
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
					nondates.append(dt_to_week(nd,sat) - 1)
			nondates.append(dt_to_week(nd,sat))
			mnths = (nd.year - dob.year) * 12 + nd.month - dob.month
			if abs(mnths - 13*12) > 2:
				nondates.append(dt_to_week(nd.replace(year=dob.year + 13),sat))
				notes += f" Added year before/after {nd.strftime('%A, %B %d, %Y')} to nondates."
			#check if it's a saturday. date.weekday() => Monday is 0, Sunday is 6
			#check if it's 13 years after birthday
			person[key] = parse(person[key]).date().strftime("%A, %B %d, %Y")
	holidates = person['holiday_dates'].split(';')
	if holidates == ['']:
		holidates = []
	for s in holidates:
		d1 = parse(s.split(' - ')[0],fuzzy=True,default=datetime.datetime.now().replace(year=2021)).date()
		d2 = parse(s.split(' - ')[0],fuzzy=True,default=datetime.datetime.now().replace(year=2020)).date()
		d3 = parse(s.split(' - ')[0],fuzzy=True,default=datetime.datetime.now().replace(year=2022)).date()
		for d in [d1,d2,d3]:
			if d.weekday() != 5:
				if d.weekday == 6:
					d = d-timedelta(days=1)
				else:
					d= dt_next_sat(d)
			nondates.append(dt_to_week(d,sat))


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
	person['days_before_sat'] = days_before_sat

# datestuff = ['dob','hfullbd','bmdate','hfullbmdate']
# pprint([{key:person[key] for key in datestuff} for person in people])
# pprint([{key:val for key,val in person.items() if key in datestuff} for person in people])

#Read extra_info.extras
for person in people:
	for k in extra_kw:
		if k not in person:
			person[k]=None
	person['requested_dates'] = []
	person['solo']=False
	person['nosummer']=False

	extra_stuff = extra.get(person['childname'])
	if extra_stuff is not None:
		for k,v in extra_stuff.items():
			person[k] = v
		if person['nosummer']==True:
			person['requested_after'] = summer_end_str
			for d in summer_dates:
				person['nondates'].append(d)
		if person['requested_after'] is not None:
			person['requested_after'] = dt_to_week(parse(person['requested_after']).date(),sat)
		if person['required_date'] is not None:
			person['required_date'] = dt_to_week(parse(person['required_date']).date(),sat)
		person['requested_dates'] = [dt_to_week(parse(d).date(),sat) for d in person['requested_dates']]
		if person['sharewith'] is not None:
			person['sharewith'] = index_by_name(person['sharewith'],people)
		if person['notsameday'] is not None:
			person['notsameday'] = [index_by_name(aname,people) for aname in person['notsameday']]
		if person['requested_after'] is not None:
			#Arbitrary - if bm requested after date, treat that date as birthday
			for d in range(person['requested_after'],person['requested_after']+ late_threshold):
				person['requested_dates'].append(d)
		if (person['required_date'] is not None) and (person['required_date'] not in person['requested_dates']):
			person['requested_dates'].append(person['required_date'])


# for person_name,extras in extra.items():
# 	person = find_by_name(person_name,people)
# 	for k in extra_kw:
# 		person[k] = extras.get(k,None)
# 	if person['requested_dates'] is None:
# 		person['requested_dates']=[]
# 	if person['nosummer']==True:
# 		person['requested_after'] = summer_end_str
# 		for d in summer_dates:
# 			person['nondates'].append(d)
# 	if person['requested_after'] is not None:
# 		person['requested_after'] = dt_to_week(parse(person['requested_after']).date(),sat)
# 	if person['required_date'] is not None:
# 		person['required_date'] = dt_to_week(parse(person['required_date']).date(),sat)
# 	person['requested_dates'] = [dt_to_week(parse(d).date(),sat) for d in person['requested_dates']]
# 	if person['sharewith'] is not None:
# 		person['sharewith'] = index_by_name(person['sharewith'],people)
# 	if person['notsameday'] is not None:
# 		person['notsameday'] = [index_by_name(aname,people) for aname in person['notsameday']]
# 	if person['requested_after'] is not None:
# 		#Arbitrary - if bm requested after date, treat that date as birthday
# 		for d in range(person['requested_after'],person['requested_after']+ late_threshold):
# 			person['requested_dates'].append(d)
# 	if (person['required_date'] is not None) and (person['required_date'] not in person['requested_dates']):
# 		person['requested_dates'].append(person['required_date'])
# print("PRINTING PEOPLE")
# pprint(people)

schools = sorted(list({person.get('school') for person in people}))
hschools = sorted(list({person.get('hschool') for person in people}))
dates = {d for person in people for d in range(person['earliest'],person['latest']+1)}| {d for person in people for d in person['requested_dates']}
# print(dates)
# print("\n".join([f"{person['childname']} : {[week_to_date(d,sat) for d in person['requested_dates'] ]}" for person in people]))
# print("\n".join([f"{person['childname']} : {[d for d in person['requested_dates'] ]}" for person in people]))
dates = sorted(list(dates))

for person in people:
	if 'lainer' in person['school'].lower():
		person['school']='The Lainer School of Sinai Temple'
	if 'lainer' in person['hschool'].lower():
		person['hschool']='The Lainer School of Sinai Temple'


date_inds = {date : i for i, date in enumerate(dates)}
for person in people:
	person['school_id'] = schools.index(person['school'])
	person['bday_index'] = date_inds[person['weeks_til']]
	person['earliest_index'] = date_inds[person['earliest']]
	person['latest_index'] = date_inds[person['latest']]
	person['date_inds'] =list(range(person['earliest_index'],person['latest_index'])) + [date_inds[thing] for thing in person['requested_dates']]
	person['requested_date_inds'] = [date_inds[thing] for thing in person['requested_dates']]
	if person['required_date'] is not None:
		person['required_date_ind'] = date_inds[person['required_date']]
	else:
		person['required_date_ind']=None
	person['nondate_inds'] = [date_inds[d] for d in person['nondates'] if (date_inds.get(d) is not None)] #ignore nondate if outside range of potential dates

# # school_date_conflicts[(school_id,d)]=[i1,i2,i3,...] contains a list of all indices of students eligible for mitzvah on day d who attend school school_id. All such lists are of length at least 2, otherwise no conflict.
# # date_prospects[d] contains a list of tuples (i,l) where for person indices i and school_id l if person i is eligible for mitzvah on date d
school_date_conflicts = {}
date_prospects = [[] for d in dates]
for i,person in enumerate(people):
	schoolid = person['school_id']
	# for d in range(person['earliest_index'],person['latest_index']):
	# print(f"date_inds: {person['date_inds']}, nondates: {person['nondates']}")
	for d in person['date_inds']:
		if any([other[1]==schoolid for other in date_prospects[d]]):
			school_date_conflicts[(schoolid,d)] = [i] + [other[0] for other in date_prospects[d] if other[1] == schoolid]
		date_prospects[d].append((i,schoolid))


venue_keys = ['pref_main','pref_family','pref_torah']
#venue ratings
for person in people:
	for preflabel in venue_keys:
		person[preflabel] = parse_pref(person[preflabel])
pref_vector = []

n = sum(((len(person['date_inds']))*venues for person in people)) # x_i_j_k is person i at venue j, date k
print("Number of decision variables (excluding extra requirements): " + str(n))

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
		for k in person['date_inds']:
			I[(i,j,k)] = ind
			Ix.append((i,j,k))
			ensure_mitzvah.append(1*x[ind])
			pref_vector.append((-1*person[venue_keys[j]])*x[ind]) #venue preferences
			# if k not in person['requested_date_inds']: #regular date
			# 	pref_vector.append((-1*person[venue_keys[j]])*x[ind]) #venue preferences
			# elif k == person['required_date_ind']: #required date
			# 	pref_vector.append((-5*person[venue_keys[j]] - 5)*x[ind]) #venue preferences
			# else: #requested date
			# 	pref_vector.append((-1*person[venue_keys[j]] - 5)*x[ind]) #venue preferences
			#set nondates equal to zero
			if k in person['nondate_inds']:
				# assignment_model += pulp.lpSum([1*x[ind]]) == 0
				assignment_model += x[ind]==0
			ind +=1
	assignment_model += pulp.lpSum(ensure_mitzvah)==1


#Lainer School not-same-day requirement
# for i,person in enumerate(people):
# 	for j in range(venues):
# 		for k in person['date_inds']:
# 			if "lainer" in person['school'].lower():
# 				for y,persony in enumerate(people):
# 					if "lainer" in persony['school']:
# 						i_ind = I[(i,j,k)]
# 						y_ind = I[(y,j,k)]
# 						assignment_model += x[i_ind] + x[y_ind] <=1



# # Lainer restrictions, attempted another way...
lainer_sums={}
for ind, (i,j,k) in enumerate(Ix):
	if k not in lainer_sums:
		lainer_sums[k]=[]
	person = people[i]
	if "lainer" in person['school'].lower():
		lainer_sums[k].append(1*x[ind])

for k,val in lainer_sums.items():
	# print(f"lainer_sums list has {len(val)} elements")
	assignment_model += pulp.lpSum(val) <= 1

# All schools, limit to one student per day - can comment out this entire block if not a true requirement
school_sums = {}
for sch in schools:
	sch_sum = {}
	school_sums[sch]= sch_sum
	for ind, (i,j,k) in enumerate(Ix):
		if k not in sch_sum:
			sch_sum[k]=[]
		person = people[i]
		if (sch.lower() in person['school'].lower()) or (person['school'].lower() in sch.lower()):
			sch_sum[k].append(1*x[ind])
	for k,val in sch_sum.items():
		# print(f"lainer_sums list has {len(val)} elements")
		assignment_model += pulp.lpSum(val) <= 1





# # Add penalty for bnei mitzvah being n weeks after birthday.
# #OPTIONAL: minimize number of venues in use per weekend? is there "pulp.lpMax" for m[ind] variables?
penalty_per_week = 1
# lateness_penalties = [penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7))*x[ind] for ind, (i,j,k) in enumerate(Ix)]
lateness_penalties =[]
for ind, (i,j,k) in enumerate(Ix):
	person = people[i]
	#weekly penalty for requested dates vs regular dates
	request_weekly_penalty_factor = 0.2
	if k not in person['requested_date_inds']: #regular date
		pen = penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7))*x[ind]
		# pref_vector.append((-1*person[venue_keys[j]])*x[ind]) #venue preferences
	elif k == person.get('required_date_ind'): #required date
		# pref_vector.append((-5*person[venue_keys[j]] - 5)*x[ind]) #venue preferences
		pen = -5*x[ind]
	else: #requested date
		# pref_vector.append((-1*person[venue_keys[j]] - 5)*x[ind]) #venue preferences
		pen = request_weekly_penalty_factor*penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7) - 3)*x[ind]
	# pen = penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7))*x[ind]
	lateness_penalties.append(pen)
#Add days before sat*(1/7) to ensure that older students receive a slightly larger penalty than younger students, enforcing which will yield earlier BMs

assignment_model += pulp.lpSum(lateness_penalties + pref_vector) #add to objective function


# school_date_conflicts[(school_id,d)]=[i1,i2,i3,...] contains a list of all indices of students eligible for mitzvah on day d who attend school school_id.
Im = {}
Imx = []
ind = 0
for ((l,k),students) in school_date_conflicts.items():
	onevenue = []
	for j in range(venues):
		Im[(j,l,k)] = ind
		Imx.append((j,l,k))
		onevenue.append(1*m[ind])
		for i in students:
			assignment_model += pulp.lpSum([1*x[I[(i,j,k)]],-1*m[ind]]) <= 0
		ind +=1
	assignment_model += pulp.lpSum(onevenue)<=1



# # Venue restrictions, attempted another way...
venue_sums={}
for ind, (i,j,k) in enumerate(Ix):
	if (j,k) not in venue_sums:
		venue_sums[(j,k)]=[]
	person = people[i]
	if person.get('solo')==True:
		# venue_sums[(j,k)].append(2*x[ind]) #real
		venue_sums[(j,k)].append(2*x[ind]) #relaxed
	else:
		venue_sums[(j,k)].append(1*x[ind])
for key,val in venue_sums.items():
	j = key[0]
	k = key[1]
	assignment_model += pulp.lpSum(val) <= venue_max[j]



assignment_model.solve()
status = assignment_model.status
statuses = {1:"optimal",0:"not solved",-1:"infeasible",-2:"unbounded",-3:"undefined"}
print(f"Status is: '{statuses[status]}'")
x =[val.varValue for k,val in x.items()]

ones = [i for i, v in enumerate(x) if v == 1]
winners = [Ix[v] for v in ones]

for (i,j,k) in winners:
	people[i]['venue'] = j
	people[i]['best_week'] = dates[k]


for person in people:
	person['venue_sharing_problem']=False
	person['solo_sharing_problem']=False
	person['lainer_sharing_problem']=False
	person['same_school_sameday']=False
	person['shared']=False
	for other in people:
		if (other['best_week']==person['best_week']) and (other['venue'] == person['venue']) and (other['childname'] != person['childname']):
			person['shared']=True
			if person['venue']!=0:
				person['venue_sharing_problem']=True
		if (other['best_week']==person['best_week']) and ('lainer' in other['school'].lower()) and ('lainer' in person['school'].lower()) and (other['childname'] != person['childname']):
			person['lainer_sharing_problem']=True
		if (other['best_week']==person['best_week']) and (other['school'] == person['school']) and (other['childname'] != person['childname']):
			person['same_school_sameday']=True
	if person['shared']==True and person['solo']==True:
		person['solo_sharing_problem']=True

for person in people:
	# person['earliest'] = (sat + relativedelta(weeks=person['earliest'])).strftime("%A, %B %d, %Y")
	# person['latest'] = (sat + relativedelta(weeks=person['latest'])).strftime("%A, %B %d, %Y")
	# person['best_week'] = (sat + relativedelta(weeks=person['best_week'])).strftime("%B %d, %Y")
	person['earliest_ind'] = person['earliest']
	person['earliest'] = week_to_date(person['earliest'],sat)
	person['latest'] = week_to_date(person['latest'],sat)
	person['best_week_ind']=person['best_week']
	person['best_week'] = week_to_date(person['best_week'],sat)
	person['nondates'] = [week_to_date(d,sat) for d in person['nondates']]
	# person['dob'] = parse(person['dob']).date()
	person['best_week'] = parse(person['best_week']).date()
	person['venue_prefs'] = [person[key] for key in ['pref_main','pref_family','pref_torah']]
	person['top_venue'] = person['venue_prefs'][person['venue']] == max(person['venue_prefs'])
	person['weeks_after_earliest'] = person['best_week_ind']-person['earliest_ind']

outfilename = infile.split('.')
outfilename[-2] +='_solution'
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=[k for k in people[0]])
	writer.writeheader()
	for person in people:
		writer.writerow(person)


optheads = ['childname','nondates','accommodations','more_info','more_info','notes','dob','gbmbd','venue_prefs','top_venue','weeks_after_earliest','school','venue','best_week','shared','venue_sharing_problem','solo','solo_sharing_problem','lainer_sharing_problem','same_school_sameday']
outfilename = infile.split('.')
outfilename[-2] +='_solution_basic'
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=optheads)
	writer.writeheader()
	for person in people:
		writer.writerow({key:person[key] for key in optheads})
# pprint(people)





