import csv
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime
import pulp

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']


early_threshold = 1 # number weeks before birthday allowed
late_threshold = 5 # number of weeks after birthday at which mitzvah is not allowed
venues = 3
venue_max = 2 # max number of mitzvahs per venue per day


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
	return users


#Monday is 0, Saturday is 5, Sunday is 6
def next_sat(dt):
	return dt + relativedelta(days = ((5 - dt.weekday()) % 7))

today = datetime.datetime.today().date()
sat = next_sat(today)

# plan['arrivalTime'] = (eventDateTime + relativedelta(minutes=arrivalMins)).isoformat()
infile = 'people.csv'
constraints = readfile('constraints.csv')
people = readfile(infile)

for person in people:
	bnei_bday = parse(person['DOB']).date() + relativedelta(years=12 if person.get('Gender')=='f' else 13)
	person['bnei_bday'] = bnei_bday.strftime("%A, %B %d, %Y")
	bnei_bday_sat = next_sat(bnei_bday)
	person['weeks_til']= (bnei_bday_sat - sat).days // 7
	person['earliest'] = max(0,person['weeks_til'] - early_threshold)
	person['latest'] = person['weeks_til'] + late_threshold

schools = sorted(list({person.get('School') for person in people if person.get('School') is not None}))
dates = sorted(list({d for person in people for d in range(person['earliest'],person['latest']+1)}))
date_inds = {date : i for i, date in enumerate(dates)}
for person in people:
	person['bday_index'] = date_inds[person['weeks_til']]
	person['earliest_index'] = date_inds[person['earliest']]
	person['latest_index'] = date_inds[person['latest']]
	person['school_id'] = schools.index(person['School'])

# school_date_conflicts[(school_id,d)]=[i1,i2,i3,...] contains a list of all indices of students eligible for mitzvah on day d who attend school school_id. All such lists are of length at least 2, otherwise no conflict.
# date_prospects[d] contains a list of tuples (i,l) where for person indices i and school_id l if person i is eligible for mitzvah on date d
school_date_conflicts = {}
date_prospects = [[] for d in dates]
for i,person in enumerate(people):
	for d in range(person['earliest_index'],person['latest_index']):
		if any([other[1]==person['school_id'] for other in date_prospects[d]]):
			school_date_conflicts[(person['school_id'],d)] = [i] + [other[0] for other in date_prospects[d] if other[1] == person['school_id']]
		date_prospects[d].append((i,person['school_id']))

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
			ind +=1
	assignment_model += pulp.lpSum(ensure_mitzvah)==1

# Add penalty for bnei mitzvah being n weeks after birthday.
#OPTIONAL: minimize number of venues in use per weekend? is there "pulp.lpMax" for m[ind] variables?
penalty_per_week = 1
lateness_penalties = [penalty_per_week*(abs(dates[k]-people[i]['weeks_til']))*x[ind] for ind, (i,j,k) in enumerate(Ix)]
assignment_model += pulp.lpSum(lateness_penalties)

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

# Each venue can host at maximum venue_max mitzvahs in a day
for k,date_student_school_tuples in enumerate(date_prospects):
	if len(date_student_school_tuples) > venue_max:
		for j in range(venues):
			venuelimit = []
			for (i,l) in date_student_school_tuples:
				venuelimit.append(1*x[I[(i,j,k)]])
			assignment_model += pulp.lpSum(venuelimit) <= venue_max

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
	person['best_week'] = (sat + relativedelta(weeks=person['best_week'])).strftime("%A, %B %d, %Y")
	del person['earliest_index']
	del person['latest_index']
	del person['bday_index']
	del person['school_id']
	del person['earliest']
	del person['latest']

outfilename = infile.split('.')
outfilename[-2] +='_solution'
outfilename = '.'.join(outfilename)
outfile = open(outfilename,'w')
with outfile:
	writer = csv.DictWriter(outfile, fieldnames=[k for k in people[0]])
	writer.writeheader()
	for person in people:
		writer.writerow(person)

pprint(people)
