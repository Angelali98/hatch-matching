import csv
import heapq

#FELLOWS 
#############################################################################################################

#sort fellows into buckets of subjects by level of education 
def addFellow(row):
    #if lower elementary then iterate over the subjects and place in the lower elementary bucket 
    subjects = row['subjects'].split(', ')
    grades = row['grades'].split(', ')
    for grade in grades: 
        if grade == 'Lower elementary school (Grades K-2)': 
            for subject in subjects: 
                if subject in low_elementary:
                    ###add TF to the set 
                    low_elementary[subject].add((-int(tut_count), row['name']))
        #if higher elementary then iterate over the subjects and place in the higher elementary bucket 
        if grade == 'Upper elementary school (Grades 3-5)': 
            for subject in subjects: 
                if subject in high_elementary:
                    ###add TF to the set 
                    high_elementary[subject].add((-int(tut_count), row['name']))
        #if middle then iterate over the subjects and place in the middle school bucket 
        if grade == 'Middle school': 
            for subject in subjects: 
                if subject in middle:
                    ###add TF to the set 
                    middle[subject].add((-int(tut_count), row['name']))
        #if high then iterate over the subjects and place in the high school bucket 
        if grade == 'High school': 
            for subject in subjects: 
                if subject in high:
                    ###add TF to the set 
                    high[subject].add((-int(tut_count), row['name']))

# remove given fellow from all subject buckets 
def removeFellow(fellow): 
    fellow_info = fellows[fellow]
    subjects = fellow_info['subjects'].split(', ')
    grades = fellow_info['grades'].split(', ')
    for grade in grades: 
        if grade == 'Lower elementary school (Grades K-2)': 
            for subject in subjects: 
                if subject in low_elementary:
                    ###remove TF from the set 
                    low_elementary[subject].remove((-1, fellow))
        #if higher elementary then iterate over the subjects and place in the higher elementary bucket 
        if grade == 'Upper elementary school (Grades 3-5)': 
            for subject in subjects: 
                if subject in high_elementary:
                    high_elementary[subject].remove((-1, fellow))
        #if middle then iterate over the subjects and place in the middle school bucket 
        if grade == 'Middle school': 
            for subject in subjects: 
                if subject in middle:
                    middle[subject].remove((-1, fellow))
        #if high then iterate over the subjects and place in the high school bucket 
        if grade == 'High school': 
            for subject in subjects: 
                if subject in high:
                    high[subject].remove((-1, fellow))

# update tutee capacity for all subject buckets for given fellow to capacity 
def updateCapacity(fellow, capacity):
    fellow_info = fellows[fellow]
    subjects = fellow_info['subjects'].split(', ')
    grades = fellow_info['grades'].split(', ')
    tut_count = capacity-1
    for grade in grades: 
        if grade == 'Lower elementary school (Grades K-2)': 
            for subject in subjects: 
                if subject in low_elementary:
                    ###remove TF from the set 
                    low_elementary[subject].remove((tut_count, fellow))
                    low_elementary[subject].add((capacity, fellow))
        #if higher elementary then iterate over the subjects and place in the higher elementary bucket 
        if grade == 'Upper elementary school (Grades 3-5)': 
            for subject in subjects: 
                if subject in high_elementary:
                    high_elementary[subject].remove((tut_count, fellow))
                    high_elementary[subject].add((capacity, fellow))
        #if middle then iterate over the subjects and place in the middle school bucket 
        if grade == 'Middle school': 
            for subject in subjects: 
                if subject in middle:
                    middle[subject].remove((tut_count, fellow))
                    middle[subject].add((capacity, fellow))
        #if high then iterate over the subjects and place in the high school bucket 
        if grade == 'High school': 
            for subject in subjects: 
                if subject in high:
                    high[subject].remove((tut_count, fellow))
                    high[subject].add((capacity, fellow))

# one dictonary to hold each fellow as key and their row as the value 
fellows = {}

# track fellows and their tutee capacity and their matches, initialize to total capacity.
# Key is the fellow name as string, the value is a list which is capacity + list of tutees 
matches = {}

#hash of all elementary subjects as key and value is list of fellows that can teach the subject
low_elementary = {"English Reading": set([]), "English Writing": set([]), "Math (up to Algebra)": set([]), 
"History": set([]), "Computer Science": set([]), "Spanish": set([]), "French": set([]), "Chinese": set([])}

high_elementary = {"English Reading": set([]), "English Writing": set([]), "Math (up to Algebra)": set([]), 
"History": set([]), "Computer Science": set([]), "Spanish": set([]), "French": set([]), "Chinese": set([])}

#hash of all middle school subjects as key and list is fellows 
middle = {"English Reading": set([]), "English Writing": set([]), "Math (up to Algebra)": set([]), 
"History": set([]), "Biology": set([]), "Chemistry": set([]), "Physics": set([]), "Computer Science": set([]), 
"Spanish": set([]), "French": set([]), "Chinese": set([]), "Geometry": set([]), "SAT Reading": set([]),
"SAT Math": set([]), "SAT Writing": set([]), "ACT English": set([]), "ACT Math": set([]), "ACT Reading": set([]),
"ACT Science": set([]), "ACT Writing": set([])}

#hash of all elementary subjects as key and list is fellows 
high = {"English Reading": set([]), "English Writing": set([]), "Math (up to Algebra)": set([]), "Geometry": set([]), 
"Calculus": set([]), "History": set([]), "Biology": set([]), "Chemistry": set([]), "Physics": set([]),
"Computer Science": set([]), "Spanish": set([]), "French": set([]), "Chinese": set([]), "SAT Reading": set([]),
"SAT Math": set([]), "SAT Writing": set([]), "ACT English": set([]), "ACT Math": set([]), "ACT Reading": set([]),
"ACT Science": set([]), "ACT Writing": set([]), "College Applications": set([])}

#open fellows csv and parse information
with open('fellows.csv', mode='r') as fellowcsv:
    fellowreader = csv.DictReader(fellowcsv)
    for row in fellowreader:
        # populate the fellows dictionary
        tut_count = row['tut_count']
        if tut_count == 'More than 3':
            tut_count = 4
        fellows[row['name']] = row
        matches[row['name']] = [tut_count]
        #add the fellow to the subject buckets by grade level based on the subjects they indicate 
        addFellow(row)
        

# FELLOWS HAVE BEEN PARSED
# ORDER THE SUBJECT BUCKETS TO PREPARE FOR MATCHING
####################################################################################################

# Create a minheap of subjects ordered by number of fellows per subject. 
# First item = the subject with least number of tfs 
# Each object is a tuple: int = length of fellows in bucket, string = subject name, string = grade level name
def makeHeap(heap, gradelist, gradename):
    for subject, fellows in gradelist.items():
        length = len(fellows)
        heapq.heappush(heap, (length, subject, gradename))

# add all the subject counts together into a new list and heapify it so subject with least available fellows is matched first
subj_counts = []
makeHeap(subj_counts, low_elementary, "Lower elementary")
makeHeap(subj_counts, high_elementary, "Higher elementary")
makeHeap(subj_counts, middle, "Middle")
makeHeap(subj_counts, high, "High")


# TUTEES PARSING
######################################TUTEES######################################################

#create a dictionary that holds each tutee as a key and their row as the value
tutees = {}

#track unmatched students 
unmatched = set([])

#create a list of buckets, each bucket represents a subject and the list of tutees is the values 
low_elementary_tutee = {}
high_elementary_tutee = {}
middle_tutee = {}
high_tutee = {}

#clear out the buckets for every subject for every grade level
def clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee):
    low_elementary_tutee['English Reading'] = []
    low_elementary_tutee['English Writing'] = []
    low_elementary_tutee['Math (up to Algebra)'] = []
    low_elementary_tutee['History'] = []
    low_elementary_tutee['Computer Science'] = []
    low_elementary_tutee['Spanish'] = []
    low_elementary_tutee['French'] = []
    low_elementary_tutee['Chinese'] = []
    low_elementary_tutee['Other'] = []

    high_elementary_tutee['English Reading'] = []
    high_elementary_tutee['English Writing'] = []
    high_elementary_tutee['Math (up to Algebra)'] = []
    high_elementary_tutee['History'] = []
    high_elementary_tutee['Computer Science'] = []
    high_elementary_tutee['Spanish'] = []
    high_elementary_tutee['French'] = []
    high_elementary_tutee['Chinese'] = []
    high_elementary_tutee['Other'] = []

    middle_tutee['English Reading'] = []
    middle_tutee['English Writing'] = []
    middle_tutee['Math (up to Algebra)'] = []
    middle_tutee['History'] = []
    middle_tutee['Computer Science'] = []
    middle_tutee['Spanish'] = []
    middle_tutee['French'] = []
    middle_tutee['Chinese'] = []
    middle_tutee['Biology'] = []
    middle_tutee['Chemistry'] = []
    middle_tutee['Physics'] = []
    middle_tutee['Geometry'] = []
    middle_tutee['Other'] = []
    middle_tutee['SAT Reading'] = []
    middle_tutee['SAT Math'] = []
    middle_tutee['SAT Writing'] = []
    middle_tutee['ACT Math'] = []
    middle_tutee['ACT Reading'] = []
    middle_tutee['ACT English'] = []
    middle_tutee['ACT Writing'] = []
    middle_tutee['ACT Science'] = []

    high_tutee['English Reading'] = []
    high_tutee['English Writing'] = []
    high_tutee['Math (up to Algebra)'] = []
    high_tutee['History'] = []
    high_tutee['Computer Science'] = []
    high_tutee['Spanish'] = []
    high_tutee['French'] = []
    high_tutee['Chinese'] = []
    high_tutee['Biology'] = []
    high_tutee['Chemistry'] = []
    high_tutee['Physics'] = []
    high_tutee['Geometry'] = []
    high_tutee['Calculus'] = []
    high_tutee['SAT Reading'] = []
    high_tutee['SAT Math'] = []
    high_tutee['SAT Writing'] = []
    high_tutee['ACT Math'] = []
    high_tutee['ACT Reading'] = []
    high_tutee['ACT English'] = []
    high_tutee['ACT Writing'] = []
    high_tutee['ACT Science'] = []
    high_tutee['College Applications'] = []
    high_tutee['SAT'] = []
    high_tutee['ACT'] = []
    high_tutee['Other'] = []

# given the row that contains all the information for a tutee and the #choice of subject
# output the subject and evaluation for that subject
def TuteeInfoByChoice(info, choice):
    if choice == 1:
        subject = info['Subject1']
        evaluation = info['Evaluation1']
        return subject, evaluation
    if choice == 2:
        subject = info['Subject2']
        evaluation = info['Evaluation2']
        return subject, evaluation
    if choice == 3: 
        subject = info['Subject3']
        evaluation = info['Evaluation3']
        return subject, evaluation


# given the set of unmatched tutees, put them into the proper subject level buckets by grade level 
# insert a tuple = the evaluation for the subject with tutee name
def makeTuteeBucket(unmatched, choice, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees):

    unmatched_list = list(unmatched)
    for tutee in unmatched_list:
        info = tutees[tutee]    
        subject, evaluation = TuteeInfoByChoice(info, choice) #######TEST CORNER CASES IF ANY OF THESE FIELDS ARE BLANK
        if subject == '':
            continue 
        if evaluation == '':
            evalutation = 5
        if info['Grade'] == 'Kindergarten' or info['Grade'] == '1st Grade' or info['Grade'] == '2nd Grade':
            heapq.heappush(low_elementary_tutee[subject], (int(evaluation), tutee))
        if info['Grade'] == '3rd Grade' or info['Grade'] == '4th Grade' or info['Grade'] == '5th Grade':
            heapq.heappush(high_elementary_tutee[subject], (int(evaluation), tutee))
        if info['Grade'] == '6th Grade' or info['Grade'] == '7th Grade' or info['Grade'] == '8th Grade':
            heapq.heappush(middle_tutee[subject], (int(evaluation), tutee))
        if info['Grade'] == '9th Grade' or info['Grade'] == '10th Grade' or info['Grade'] == '11th Grade' or info['Grade'] == '12th Grade':
            heapq.heappush(high_tutee[subject], (int(evaluation), tutee))

    return unmatched_list

#open tutees csv and parse  
with open('tutees.csv', mode='r') as tuteecsv:
    tuteereader = csv.DictReader(tuteecsv)
    for row in tuteereader:
        if row['Student'] == "":
            continue
        tutees[row['Student']] = row
        unmatched.add(row['Student'])

#MATCHING
#########################################################################################################################

# update the minheap subj_counts which tracks number of fellows available per subject 
# first item = subject with minimum number of fellows available 
def updateSubjectCounts(subj_counts, low_elementary, high_elementary, middle, high):
    makeHeap(subj_counts, low_elementary, "Lower elementary")
    makeHeap(subj_counts, high_elementary, "Higher elementary")
    makeHeap(subj_counts, middle, "Middle")
    makeHeap(subj_counts, high, "High")
    return subj_counts

# called by checkMatchCriterea 
# perform the necessary actions per a tutee and fellow when they are paired
# remove tutee from unmatched list and update fellow capacities
def makeMatch(multiple, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap):
    unmatched.remove(tutee) #take the tutee out of the unmatched list
    matches[fellow].append((tutee, choice)) #put in matches list with choice number
    tut_count += 1 #lower fellows capacity
    if tut_count == 0: #if capacity zero then remove tf from all subject sets they are in 
        removeFellow(fellow)
    else: #otherwise push the (capacity, fellow) back into the heap
        heapq.heappush(fellow_heap, (tut_count,fellow)) 
        updateCapacity(fellow, tut_count)

# return the platform and availability of tutee
def getTuteeInfo(tutee):
    t_info = tutees[tutee]
    tutee_platform = t_info['Platform'].split(', ')
    tutee_availability = t_info['Availability'].split(', ')
    return tutee_platform, tutee_availability

# return the platform and availability of the fellow
def getFellowInfo(fellow):
    f_info = fellows[fellow]
    fellow_platform = set(f_info['platform'].split(', '))
    fellow_availability = set(f_info['availability'].split(', '))
    return fellow_platform, fellow_availability

# called by matchGrades
# check if the platform and availability match between a tutee and fellow
def checkMatchCriterea(multiple, tutee_platform, fellow_platform, tutee_availability, fellow_availability, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap):
    for platform in tutee_platform:
        if platform in fellow_platform:
            for availability in tutee_availability:
                if availability in fellow_availability:
                    makeMatch(multiple, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap)
                    return True            
    return False

# called by the main match function 
# given a list of fellows and list of tutees per a specific subject and the choice
# iterate through the tutees and fellows to find matches
def matchGrades(multiple, fellow_candidates, tutee_candidates, choice):
    fellow_heap = list(fellow_candidates)
    heapq.heapify(fellow_heap)
        
    #iterate tutees to get matched
    for tutee_cand in tutee_candidates:
        evaluation, tutee = tutee_cand
        #get the information of the tutee
        tutee_platform, tutee_availability = getTuteeInfo(tutee)
        matched = False 
        
        #iterate the tutors one by one and check platform, availability, timezone
        for i in range(len(fellow_heap)):
            fellow_info = heapq.heappop(fellow_heap)
            tut_count, fellow = fellow_info
            #check if matched 
            if not multiple:
                values = matches[fellow]
                if len(values) > 1:
                    continue
            #get fellow information
            fellow_platform, fellow_availability = getFellowInfo(fellow)
            #do the matching
            matched = checkMatchCriterea(multiple, tutee_platform, fellow_platform, tutee_availability, fellow_availability, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap)
            if matched: 
                break  

############MATCHING FUNCTION
#match the smallest amount of TF capacity subjects first
#iterate the minheap by matching the subjects with the least number of fellows available first 
#fellows per a subject are ordered by highest capacity
#the tutees with the min eval scores are matched to the fellows with the highest capacity first
def match(multiple, choice, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high):
    #update subject bucket counts (number of fellows) 
    if choice != 1: 
        updateSubjectCounts(subj_counts, low_elementary, high_elementary, middle, high)
    
    #create matchings for the subject with least tfs first 
    for i in range(len(subj_counts)):
        subjectbucket = heapq.heappop(subj_counts)
        count, subject, grade = subjectbucket
        # if zero tfs then skip this subject
        if count == 0:
            continue 
        if grade == 'Lower elementary':
            # get all the tutee candidates for this subject
            tutee_candidates = low_elementary_tutee[subject]
            if len(tutee_candidates) == 0:
                continue
            #get the fellows and order by largest capacity
            fellow_candidates = low_elementary[subject]
            matchGrades(multiple, fellow_candidates, tutee_candidates, choice)
        if grade == 'Higher elementary':
            # get all the tutee candidates for this subject
            tutee_candidates = high_elementary_tutee[subject]
            if len(tutee_candidates) == 0:
                continue
            #get the fellows and order by largest capacity
            fellow_candidates = high_elementary[subject]
            matchGrades(multiple, fellow_candidates, tutee_candidates, choice)
        if grade == 'Middle':
            # get all the tutee candidates for this subject
            tutee_candidates = middle_tutee[subject]
            if len(tutee_candidates) == 0:
                continue
            #get the fellows and order by largest capacity
            fellow_candidates = middle[subject]
            matchGrades(multiple, fellow_candidates, tutee_candidates, choice)
        if grade == 'High':
            # get all the tutee candidates for this subject
            tutee_candidates = high_tutee[subject]
            if len(tutee_candidates) == 0:
                continue
            #get the fellows and order by largest capacity
            fellow_candidates = high[subject]
            matchGrades(multiple, fellow_candidates, tutee_candidates, choice)


# RUN THE ALGORITHM
#########################################################################################################################

#run matching for first choice by trying to match each fellow to one tutee first 
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 1, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
print("BREAK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
match(False, 1, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

#run matching for first choice allowing multiple tutees per fellow
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 1, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
print("BREAK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
match(True, 1, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

#run matching for second choice
print("BREAK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEE TWICEEEEEEEEEEEEEEEEEEEE")
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 2, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
match(True, 2, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

#run matching for third choice
print("BREAK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEE TWICEEEEEEEEEEEEEEEEEEEE")
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 3, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
match(True, 3, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

# PRINT TO TERMINAL
#########################################################################################################################
for key, value in matches.items():
    print(key, value)
print(unmatched)
for key, value in matches.items():
    if len(value) == 1:
        print(key)

# WRITE RESULTS OF ALGORITHM TO CSV
#########################################################################################################################
#field names 
fields = ['Fellow', 'Tutee', 'Choice', 'Grade', 'Subject', 'Evaluation', 'Fellow college', 'Fellow Graduation', 'Fellow Platform', 'Fellow Availbility', 'Fellow Grades', 'Fellow Subjects', 'Fellow Tutee Count']
filename = "matches.csv"

#writing to file
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for fellow, value in matches.items():
        for i in range(1,len(value)):
            tutee_info = value[i]
            tutee, choice = tutee_info
            info = tutees[tutee]
            grade = info['Grade']
            fellow_info = fellows[fellow]

            subject, evaluation = TuteeInfoByChoice(info, choice)
            row = [fellow, tutee, choice, grade, subject, evaluation, fellow_info['college'], fellow_info['graduation'], fellow_info['platform'], fellow_info['availability'], fellow_info['grades'], fellow_info['subjects'], fellow_info['tut_count']]
            csvwriter.writerow(row)



"""
# track number of fellows in each subject bucket for low elementary 
subj_count_low_elem = {"English Reading": 0, "English Writing": 0, "Math (up to Algebra)": 0, 
"History": 0, "Computer Science": 0, "Spanish": 0, "French": 0, "Chinese": 0}

# track number of fellows in each subject bucket for high elementary 
subj_count_high_elem = {"English Reading": 0, "English Writing": 0, "Math (up to Algebra)": 0, 
"History": 0, "Computer Science": 0, "Spanish": 0, "French": 0, "Chinese": 0}

# track number of fellows in each subject bucket for middle 
subj_count_middle = {"English Reading": 0, "English Writing": 0, "Math (up to Algebra)": 0, 
"History": 0, "Biology": 0, "Chemistry": 0, "Physics": 0, "Computer Science": 0, 
"Spanish": 0, "French": 0, "Chinese": 0}

# track number of fellows in each subject bucket for high 
subj_count_high = {"English Reading": 0, "English Writing": 0, "Math (up to Algebra)": 0, "Geometry": 0, 
"Calculus": 0, "History": 0, "Biology": 0, "Chemistry": 0, "Physics": 0,
"Computer Science": 0, "Spanish": 0, "French": 0, "Chinese": 0, "SAT Reading": 0,
"SAT Math": 0, "SAT Writing": 0, "ACT English": 0, "ACT Math": 0, "ACT Reading": 0,
"ACT Science": 0, "ACT Writing": 0, "College Applications": 0}"""



##### buckets for tutees 
"""low_elementary_tutee = {"English Reading": [], "English Writing": [], "Math (up to Algebra)": [], 
"History": [], "Computer Science": [], "Spanish": [], "French": [], "Chinese": []}

high_elementary_tutee = {"English Reading": [], "English Writing": [], "Math (up to Algebra)": [], 
"History": [], "Computer Science": [], "Spanish": [], "French": [], "Chinese": []}

#hash of all middle school subjects as key and list is fellows 
middle_tutee = {"English Reading": [], "English Writing": [], "Math (up to Algebra)": [], 
"History": [], "Biology": [], "Chemistry": [], "Physics": [], "Computer Science": [], 
"Spanish": [], "French": [], "Chinese": []}

#hash of all elementary subjects as key and list is fellows 
high_tutee = {"English Reading": [], "English Writing": [], "Math (up to Algebra)": [], "Geometry": [], 
"Calculus": [], "History": [], "Biology": [], "Chemistry": [], "Physics": [],
"Computer Science": [], "Spanish": [], "French": [], "Chinese": [], "SAT Reading": [],
"SAT Math": [], "SAT Writing": [], "ACT English": [], "ACT Math": [], "ACT Reading": [],
"ACT Science": [], "ACT Writing": [], "College Applications": []}"""