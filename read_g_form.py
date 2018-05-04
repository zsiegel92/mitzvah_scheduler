import sys
import csv
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date, timedelta
from convertdate import hebrew
import pulp
from Google_Submissions.extra_info import extra_kw, extra, blackouts,cycle_blackouts,cycle_blackouts2,venue_date_reserved#,extra_defaults


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
venue_names = ['Main Sanctuary','Family Minyan','Torah in the Round']

early_threshold = 0 # number weeks before birthday allowed
late_threshold = 50 # number of weeks after birthday at which mitzvah is not allowed
request_after_late_threshold = 4
request_weekly_penalty_factor = 1
constant_request_reward = 5
required_reward = 5
penalty_per_week = 2
pref_reward=2
venue_opening_penalty = 0.01 #to try to coerce shared BMs


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
	def users_same(u,o):
		return (u['email']==o['email']) and ((u['childname'].lower() in o['childname'].lower()) or ((o['childname'].lower() in u['childname'].lower())))
	filein = open(filename, 'r')
	reader = csv.reader(filein)
	headers = next(reader, None)
	users = [{headers[i] : row[i] for i in range(len(headers)) if ((row[i] is not None) and (row[i] is not ''))} for row in reader]
	filein.seek(0)
	next(reader, None)
	xheads=['xx','holiday1','holiday2','holiday3','holiday4','holiday5','holiday6','holiday7']
	cleanusers = [{heads[i] : row[i] for i in range(len(heads)) if heads[i] not in xheads} for row in reader]

	to_remove=[]
	for i,user in enumerate(cleanusers):
		for other in cleanusers:
			if users_same(user,other):
				if (parse(user['timestamp']) < parse(other['timestamp'])):
					to_remove.append(i)
	to_remove=list(set(to_remove))
	cleanusers = [v for i,v in enumerate(cleanusers) if i not in to_remove]

	return users, headers,cleanusers


def plus_thirteen(greg):
	greg2 = greg + timedelta(days=1)
	(hy,hm,hd)= hebrew.from_gregorian(greg2.year,greg2.month,greg2.day)
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
	greg2 = greg + timedelta(days=1)
	(hy,hm,hd)= hebrew.from_gregorian(greg2.year,greg2.month,greg2.day)
	h = hebrew.to_jd_gregorianyear(greg2.year+13,hm,hd)
	print(f"Converted gregorian {greg2} to hebrew {h}")
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
def pack(y,m,d):
	return date(y,m,d)

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
summer_range = (parse(summer_start_str).date(),parse(summer_end_str).date())
summer_start = dt_to_week(parse(summer_start_str).date(),sat)
summer_length = 10
summer_dates = list(range(summer_start,summer_start + summer_length + 1))
# plan['arrivalTime'] = (eventDateTime + relativedelta(minutes=arrivalMins)).isoformat()
infile = 'Google_Submissions/Mitzvah Scheduling.csv'
# constraints = readfile('constraints.csv')
people_raw, headers,people = readfile(infile)


cycle_blackout_index=2
print(sys.argv)
if len(sys.argv)>1:
	try:
		cycleinput = int(sys.argv[1])
		print(f"BLACKOUT {cycle_blackouts[cycleinput]}")
		cycle_blackout_index=cycleinput
	except Exception as ee:
		print(ee)
		print("Failed to read input")

cycle_blackout_index2=0
print(sys.argv)
if len(sys.argv)>2:
	try:
		cycleinput2 = int(sys.argv[2])
		print(f"BLACKOUT2 {cycle_blackouts2[cycleinput2]}")
		cycle_blackout_index2=cycleinput
	except Exception as ee:
		print(ee)
		print("Failed to read input")




blackouts.append(cycle_blackouts[cycle_blackout_index])
blackouts.append(cycle_blackouts2[cycle_blackout_index2])
blackout_inds = [dt_to_week(parse(d).date(),sat) for d in blackouts]


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

	nondates = list(set(nondates + blackout_inds))

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

num_unknown_schools = 0


#Read extra_info.extras
for person in people:
	if (person['school'] is None) or (person['school'] == '') or ('school' not in person):
		person['school'] = f"unknown_{num_unknown_schools}"
		num_unknown_schools += 1
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
			for d in range(person['requested_after'],person['requested_after']+ request_after_late_threshold):
				person['requested_dates'].append(d)
		if (person['required_date'] is not None) and (person['required_date'] not in person['requested_dates']):
			person['requested_dates'].append(person['required_date'])
		if person['exactrequest'] is True:
			person['requested_dates'].append(person['weeks_til']) #in format of requested_dates


for person in people:
	if 'lainer' in person['school'].lower():
		person['school']='The Lainer School of Sinai Temple'
	if 'lainer' in person['hschool'].lower():
		person['hschool']='The Lainer School of Sinai Temple'


schools = sorted(list({person.get('school') for person in people}))
hschools = sorted(list({person.get('hschool') for person in people}))
dates = {d for person in people for d in range(person['earliest'],person['latest']+1)}| {d for person in people for d in person['requested_dates']}

# print(dates)
# print("\n".join([f"{person['childname']} : {[week_to_date(d,sat) for d in person['requested_dates'] ]}" for person in people]))
# print("\n".join([f"{person['childname']} : {[d for d in person['requested_dates'] ]}" for person in people]))
dates = sorted(list(dates))
date_inds = {date : k for k, date in enumerate(dates)}


for person in people:
	person['school_id'] = schools.index(person['school'])
	person['bday_index'] = date_inds[person['weeks_til']]
	person['earliest_index'] = date_inds[person['earliest']]
	early_ind = person['earliest_index']
	person['latest_index'] = date_inds[person['latest']]
	person['date_inds'] =list(range(person['earliest_index'],person['latest_index'])) + [date_inds[thing] for thing in person['requested_dates'] if date_inds[thing]>=early_ind]
	person['requested_date_inds'] = [date_inds[thing] for thing in person['requested_dates'] if date_inds[thing]>=early_ind]
	# Remove 'if' statements in last two lines to allow requests for dates before "birthday+1" (such as "birthday")
	if person['required_date'] is not None:
		person['required_date_ind'] = date_inds[person['required_date']]
	else:
		person['required_date_ind']=None
	person['nondate_inds'] = [date_inds[d] for d in person['nondates'] if (date_inds.get(d) is not None)] #ignore nondate if outside range of potential dates


#already_reserved contains (j,k) tuples of (date,venue)
already_reserved =[]
for key,val in venue_date_reserved.items():
	j = val['required_venue']
	dstring = val['required_date']

	print(f"BLACKING OUT {dstring} AT {venue_names[j]}")

	dt = parse(dstring).date()
	d = dt_to_week(dt,sat)
	if d in date_inds:
		k = date_inds[d]
		already_reserved.append((j,k))
	else:
		print("(this date is naturally free)")
already_reserved_counts ={tup:already_reserved.count(tup) for tup in set(already_reserved)}
print(already_reserved_counts)
# twin & shared handling
to_remove = []
to_save = []
for person in people:
	shared = None
	if ("sharewith" in person) and (person['sharewith'] is not None) and (person['sharewith'] != -1):
		shared = people[person['sharewith']]
	if shared is not None:
		person['nondates'] = sorted(list(set(person['nondates'] + shared['nondates'])))
		person['solo'] = True
		shared['solo'] = True
		if shared  in to_save:
			pass
		else:
			person['childname'] += f" and {shared['childname']} ({shared['email']})"
			person['accommodations'] += f" (for {shared['childname']} - '{shared['accommodations']}')"
			person['more_info'] += f" (for {shared['childname']} - '{shared['more_info']}')"
			to_remove.append(shared)
			to_save.append(person)
	if 'yes' in person['twin'].lower():
		person['solo'] = True
print(f"len people: {len(people)}")
for person in to_remove:
	if person in people:
		people.remove(person)
print(f"len people: {len(people)}")



## DONE ALTERING people

students_by_school = [[i for i,person in enumerate(people) if person['school_id']==l] for l,school in enumerate(schools)]

# for l,schname in enumerate(schools):
# 	print(f"{schname}: {list(map(lambda i:people[i]['childname'],students_by_school[l]))}\n")





# # school_date_conflicts[(school_id,d)]=[i1,i2,i3,...] contains a list of all indices of students eligible for mitzvah on day d who attend school school_id. All such lists are of length at least 2, otherwise no conflict.
# # date_prospects[d] contains a list of tuples (i,l) where for person indices i and school_id l if person i is eligible for mitzvah on date d
school_date_conflicts = {}
date_prospects = [[] for d,k in date_inds.items()]
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


n = sum(((len(person['date_inds']))*venues for person in people)) # x_i_j_k is person i at venue j, date k
x=pulp.LpVariable.dicts('assignments',range(0,n),lowBound=0,upBound=1,cat=pulp.LpBinary)
# m=pulp.LpVariable.dicts('school-date-limits',range(0,len(school_date_conflicts)*venues),lowBound=0,upBound=1,cat=pulp.LpBinary)
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
			#set nondates equal to zero
			if k in person['nondate_inds']:
				# assignment_model += pulp.lpSum([1*x[ind]]) == 0
				assignment_model += x[ind]==0

			#venue_date_reserved something something

			ind +=1
	# assignment_model += pulp.lpSum(ensure_mitzvah)==1

ensure_mitzvah = [[] for person in people]
pref_vector = []
for ind, (i,j,k) in enumerate(Ix):
	ensure_mitzvah[i].append(1*x[ind])
	person = people[i]
	pref_vector.append((-pref_reward*person[venue_keys[j]])*x[ind])
for ls in ensure_mitzvah:
	assignment_model += pulp.lpSum(ls)==1


# # Lainer students - no more than 2 same day. Actually goes for all schools.
# # Can comment/uncomment ALL of this
lainer_sums={}
for ind, (i,j,k) in enumerate(Ix):
	if k not in lainer_sums:
		lainer_sums[k]=[]
	person = people[i]
	if "lainer" in person['school'].lower():
		if ('yes' in person['twin'].lower()) or (person.get('solo')==True):
			lainer_sums[k].append(2*x[ind])
		else:
			lainer_sums[k].append(1*x[ind])
for k,val in lainer_sums.items():
	assignment_model += pulp.lpSum(val) <= 2

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
		assignment_model += pulp.lpSum(val) <= 2 #can be 0, potential numeric issue






# # Add penalty for bnei mitzvah being n weeks after birthday.
# #OPTIONAL: minimize number of venues in use per weekend? is there "pulp.lpMax" for m[ind] variables?
# lateness_penalties = [penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7))*x[ind] for ind, (i,j,k) in enumerate(Ix)]
lateness_penalties =[]
for ind, (i,j,k) in enumerate(Ix):
	person = people[i]
	#weekly penalty for requested dates vs regular dates
	if k not in person['requested_date_inds']: #regular date
		pen = penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7))*x[ind]
		# pref_vector.append((-1*person[venue_keys[j]])*x[ind]) #venue preferences
	elif k == person.get('required_date_ind'): #required date
		# pref_vector.append((-5*person[venue_keys[j]] - 5)*x[ind]) #venue preferences
		pen = -required_reward*x[ind]
	else: #requested date
		# pref_vector.append((-1*person[venue_keys[j]] - 5)*x[ind]) #venue preferences
		pen = request_weekly_penalty_factor*penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) - constant_request_reward)*x[ind]
	# pen = penalty_per_week*((abs(dates[k]-people[i]['weeks_til'])) + person['days_before_sat']*(1/7))*x[ind]
	lateness_penalties.append(pen)
#Add days before sat*(1/7) to ensure that older students receive a slightly larger penalty than younger students, enforcing which will yield earlier BMs


# school_date_conflicts[(school_id,d)]=[i1,i2,i3,...] contains a list of all indices of students eligible for mitzvah on day d who attend school school_id.
# Im = {}
# Imx = []
# ind = 0

# numconsts=0
# # for k,v in school_date_conflicts.items():
# # 	print(f"{k}: {v}")
# onevenues={}
# for ((l,k),students) in school_date_conflicts.items():
# 	onevenue = []
# 	for j in range(venues):
# 		Im[(j,l,k)] = ind
# 		Imx.append((j,l,k))
# 		onevenue.append(1*m[ind])
# 		if (l,k) not in onevenues:
# 			onevenues[(l,k)]=[]
# 		onevenues[(l,k)].append(1*m[ind])
# 		for i in students:
# 			# assignment_model += x[I[(i,j,k)]] <= m[ind]
# 			numconsts+=1
# 		ind +=1
# 	# assignment_model += pulp.lpSum(onevenue)<=1
# 	# assignment_model += pulp.lpSum(onevenues[(l,k)])<=1 #can be 0, potential numeric
# print(f"Number school-date constraints: {numconsts}")



## Ensure that each school only has students at one venue per day

# x[I[(i,j,k)]] = x_i_j_k
# Ix[I[(i,j,k)]] = (i,j,k)
# Im dict: key (j,l,k) -> index in m
# Imx list: index in m -> (j,l,k)
Im = {}
Imx = []
ind = 0
for (i,j,k) in Ix:
	l = people[i]['school_id']
	if (j,l,k) not in Imx: #or "if (j,l,k) not in Im"
		Im[(j,l,k)]=ind
		Imx.append((j,l,k))
		ind += 1
m=pulp.LpVariable.dicts('school-date-limits',range(0,len(Imx)),lowBound=0,upBound=1,cat=pulp.LpBinary)
for ind,(i,j,k) in enumerate(Ix):
	l = people[i]['school_id']
	assignment_model += x[ind] <= m[Im[(j,l,k)]]
for d,k in date_inds.items():
	for l, schname in enumerate(schools):
		schdatesum =[]
		for j in range(venues):
			if (j,l,k) in Im:
				schdatesum.append(m[Im[(j,l,k)]])
		assignment_model+= pulp.lpSum(schdatesum) <= 1

share_incentives = [venue_opening_penalty*mmm for mmm in m]


## ONLY Torah in the Round or FM can have a BM on a given day, NOT both.
# Im dict: key (j,l,k) -> index in m
# Imx list: index in m -> (j,l,k)
# Im2 dict: key (j,k) -> index in m2
# Im2x list: index in m2 -> (j,k)
# Im2 = {}
# Im2x = []
# ind = 0
# for (j,l,k) in Imx:
# 	if (j in [1,2]) and ((j,k) not in Im2x): #or "if (j,l,k) not in Im"
# 		Im2[(j,k)]=ind
# 		Im2x.append((j,k))
# 		ind += 1
# m2=pulp.LpVariable.dicts('school-date-limits',range(0,len(Im2x)),lowBound=0,upBound=1,cat=pulp.LpBinary)
# for ind,(j,l,k) in enumerate(Imx):
# 	if j in [1,2]:
# 		assignment_model += m[ind] <= m2[Im2[(j,k)]]
# for d,k in date_inds.items():
# 	venue_date_sum =[]
# 	for j in [1,2]:
# 		if (j,k) in Im2:
# 			venue_date_sum.append(m2[Im2[(j,k)]])
# 	assignment_model+= pulp.lpSum(venue_date_sum) <= 1




# # Venue restrictions
venue_sums={}
for ind, (i,j,k) in enumerate(Ix):
	if (j,k) not in venue_sums:
		venue_sums[(j,k)]=[]
	person = people[i]
	#"solo" only affects main sanctuary
	if person.get('solo')==True and (j == 0):
		venue_sums[(j,k)].append(2*x[ind])
	else:
		venue_sums[(j,k)].append(1*x[ind])
for key,val in venue_sums.items():
	j = key[0]
	k = key[1]
	assignment_model += pulp.lpSum(val) <= venue_max[j] - already_reserved_counts.get((j,k),0) #can be 0, potential numeric issue



assignment_model += pulp.lpSum(lateness_penalties + pref_vector + share_incentives) #add to objective function

print("Number of total mitzvah options: " + str(n))
print("Number of total decisions: " + str(len(x) + len(m)))
assignment_model.solve()
status = assignment_model.status
statuses = {1:"optimal",0:"not solved",-1:"infeasible",-2:"unbounded",-3:"undefined"}
print(f"Status is: '{statuses[status]}'")
x =[val.varValue for k,val in x.items()]
m = [val.varValue for k,val in m.items()]

ones = [i for i, v in enumerate(x) if v == 1]
ones_m = [i for i,v in enumerate(m) if v == 1]
winners = [Ix[v] for v in ones]
winners_m = [Imx[v] for v in ones_m]



## Logging which schools have ceremonies on which days
winnerlog={}
for (j,l,k) in winners_m:
	# week_to_date(dates[k],sat)
	d = dates[k]
	schname = schools[l]
	if d not in winnerlog:
		winnerlog[d]=[]
	winnerlog[d].append((venue_names[j],schname))

# for k,v in sorted(winnerlog.items(),key=lambda zz: zz[0]):
# 	print(f"{week_to_date(k,sat)}: {v}")



for (i,j,k) in winners:
	people[i]['venue'] = j
	people[i]['best_week'] = dates[k]
	#can uncomment this:
	people[i]['venues_schools_allowed_on_day']=[]
	if dates[k] in winnerlog:#should be
		people[i]['venues_schools_allowed_on_day'] = winnerlog[dates[k]]

for person in people:
	person['venue_sharing_problem']=False
	person['solo_sharing_problem']=False
	person['lainer_sharing_problem']=False
	person['same_school_sameday']=False
	person['same_school_sameday_dif_venues']=False
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
			if person['venue'] != other['venue']:
				person['same_school_sameday_dif_venues']=True
	if person['shared']==True and person['solo']==True:
		person['solo_sharing_problem']=True


keychanges = {'childname':'Child Name','dob':"Date of Birth",'hschool':"Hebrew School",'school':"Academic School",'over200':"Number Guests",'sameday_party':"Party on Same Day?",'twin':"Twin?","shared":"Shared Ceremony",'top_venue':'Assigned Top-Ranked Venue','gbmbd':'Thirteenth Hebrew Birthday +1 day','weeks_after_earliest':"Number of Weeks after Earliest Possible Date","same_school_sameday_dif_venues":"Sameday Problem","venues_schools_allowed_on_day":"Venues Allowed"}
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
	person['Venue']= venue_names[person['venue']]

	# person['BM DT']=person['best_week']
	person['BM Date'] = person['best_week'].strftime("%B %d, %Y")
	person['gbmbd'] = date(*person['gbmbd']).strftime("%B %d, %Y")
	person['dob']=person['dob'].strftime("%B %d, %Y")

	for k, v in keychanges.items():
		person[v]=person[k]
people = sorted(people,key = lambda person: person['best_week'])

outfilename = infile.split('.')
outfilename[-2] +='_solution'
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=[k for k in people[0]])
	writer.writeheader()
	for person in people:
		writer.writerow(person)


optheads = ['Child Name',"Date of Birth","Number Guests",'accommodations','more_info','Assigned Top-Ranked Venue',"Hebrew School","Academic School",'Venue','Thirteenth Hebrew Birthday +1 day',"Number of Weeks after Earliest Possible Date",'BM Date','Shared Ceremony']
outfilename = infile.split('.')
outfilename[-2] +='_solution_basic' + '_febblackout_' + parse(cycle_blackouts[cycle_blackout_index]).date().strftime("%m-%d") + 'springblackout_' + parse(cycle_blackouts2[cycle_blackout_index2]).date().strftime("%m-%d")
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=optheads)
	writer.writeheader()
	for person in people:
		writer.writerow({key:person[key] for key in optheads})
# pprint(people)





