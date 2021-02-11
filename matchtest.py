from matchingfunctions import *
import time
import heapq

####################################################################################################################
    # Test Matching Criterea: show that it matches on availability, grade level, subject, and platform
####################################################################################################################
####################################################################################################################
def checkSubject(tutee_subject, fellow_subjects):
    fellow_subjects = fellow_subjects.split(', ')
    if tutee_subject not in set(fellow_subjects):
        return False
    return True

def checkAvailability(tutee_avs, fellow_avs):
    fellow_avs = fellow_avs.split(', ')
    fellow_avs = set(fellow_avs)
    tutee_avs = tutee_avs.split(", ")
    for av in tutee_avs: 
        if av in fellow_avs:
            return True
    return False

def checkPlatform(tutee_platform, fellow_platform):
    fellow_platform = fellow_platform.split(', ')
    fellow_platform = set(fellow_platform)
    tutee_platform = tutee_platform.split(", ")
    for platform in tutee_platform: 
        if platform in fellow_platform:
            return True
    return False

def checkGrade(tutee_grade, fellow_grades):
    fellow_grades = fellow_grades.split(", ")
    if tutee_grade == 'Kindergarten' or tutee_grade == '1st Grade' or tutee_grade == '2nd Grade':
        if "Lower elementary school (Grades K-2)" in set(fellow_grades):
            return True
        else: return False
    if tutee_grade == '3rd Grade' or tutee_grade == '4th Grade' or tutee_grade == '5th Grade':
        if "Upper elementary school (Grades 3-5)" in set(fellow_grades):
            return True
        else: return False
    if tutee_grade == '6th Grade' or tutee_grade == '7th Grade' or tutee_grade == '8th Grade':
        if "Middle school" in set(fellow_grades):
            return True
        else: return False
    if tutee_grade == '9th Grade' or tutee_grade == '10th Grade' or tutee_grade == '11th Grade' or tutee_grade == '12th Grade':
        if "High school" in set(fellow_grades):
            return True
        else: return False

####################################################################################################################
# Stress test with large inputs
####################################################################################################################
####################################################################################################################
# general hypothetical runtime analysis using big O
# T = number of tutees
# F = number of fellows 
# Worst case runtime = O(T * F)
# Because of matchGrades()
# The function iterates through all tutees under a particular subject-grade bucket
# And for each tutee in the bucket, iterates through all the fellows until a match is found
# If no fellow matches the tutee then we have the worst case time of O(T * F)


#runtime testing
tic = time.perf_counter()

######################################################################
# check runtime on large numbers of tutees on one bucket 
#   large buckets of math and reading 
#   large buckets of elementary grade level 

###################################
# ~120 Tutees and ~150 Fellows with true dataset 
###################################
# 0.0087 seconds
# 0.0102
# 0.0089

###################################
# ~5100 Tutees and ~5800 Fellows with similar distribution of subjects, grades, platform, availabilities 
###################################
# 0.3981 seconds
# 0.4011 seconds
# 0.4019 seconds
######################################################################
# check runtime on large numbers of tutees on diverse buckets 

######################################################################
# check runtime on large number os tutees that cannot be matched ---? 

####################################################################################################################
# Test MULTIPLE variable --> assigning all tutors one tutee before multiple assignments
####################################################################################################################
####################################################################################################################

#use fellows.csv and tutees.csv

# MULTIPLE = TRUE
# match function called on:
# 1, TRUE
# 2, TRUE
# 3, TRUE
# results in matches_MULTIPLE_TRUE.csv
# fellows with largest capacity are filled FIRST

# MULTIPLE = FALSE
# 1, FALSE
# 1, TRUE
# 2, TRUE
# 3, TRUE
# results in matches_MULTIPLE_FALSE.csv
# fellows assigned one tutee first


####################################################################################################################
# check that subjects with the least fellows are assigned first 
####################################################################################################################
####################################################################################################################
# check makeHeap functionality
def checkHeap(subj_counts):
    prevcount = 0
    for i in range(len(subj_counts)):
        subjectbucket = heapq.heappop(subj_counts)
        count, subject, grade = subjectbucket
        if count < prevcount:
            print("Subject heap is out of order")
            return False
        prevcount = count 
    return True

####################################################################################################################
####################################################################################################################
####################################################################################################################

# check that matching assigns kids with the largest need first 
# call this function for each bucket in each tutee gradelist 
def checkNeed(tutee_candidates):
    preveval = 0
    #iterate tutees to get matched
    for tutee_cand in tutee_candidates:
        evaluation, tutee = tutee_cand
        if evaluation < preveval:
            print("Tutees matching: need ordering is incorrect")
            return
        preveval = evaluation
        heapq.heapush(tutee_candidates, evaluation, tutee)
    return

####################################################################################################################
####################################################################################################################
####################################################################################################################

# edge cases
# what if two fellows or two tutees have the same name? Need to have a unique identifier there ?

# inputs 
    # ensure name is not empty for fellows and tutees 
####################################################################################################################
####################################################################################################################
####################################################################################################################

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
        addFellow(row, tut_count, low_elementary, high_elementary, middle, high)


##############################MAKE HEAPS HERE

# add all the subject counts together into a new list and heapify it so subject with least available fellows is matched first
subj_counts = []
makeHeap(subj_counts, low_elementary, "Lower elementary")
makeHeap(subj_counts, high_elementary, "Higher elementary")
makeHeap(subj_counts, middle, "Middle")
makeHeap(subj_counts, high, "High")
# testing heap
checkHeap(subj_counts)
makeHeap(subj_counts, low_elementary, "Lower elementary")
makeHeap(subj_counts, high_elementary, "Higher elementary")
makeHeap(subj_counts, middle, "Middle")
makeHeap(subj_counts, high, "High")

###TUTEES
################################################################
#create a dictionary that holds each tutee as a key and their row as the value
tutees = {}

#track unmatched students 
unmatched = set([])

#create a list of buckets, each bucket represents a subject and the list of tutees is the values 
low_elementary_tutee = {}
high_elementary_tutee = {}
middle_tutee = {}
high_tutee = {}


#open tutees csv and parse  
with open('tutees.csv', mode='r') as tuteecsv:
    tuteereader = csv.DictReader(tuteecsv)
    for row in tuteereader:
        if row['Student'] == "":
            continue
        tutees[row['Student']] = row
        unmatched.add(row['Student'])



# RUN THE ALGORITHM
#########################################################################################################################

#run matching for first choice by trying to match each fellow to one tutee first 
#clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
#unmatched_list = makeTuteeBucket(unmatched, 1, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
#print("BREAK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
#match(False, 1, subj_counts, matches, unmatched, fellows, tutees, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

#run matching for first choice allowing multiple tutees per fellow
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 1, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
match(True, 1, subj_counts, matches, unmatched, fellows, tutees, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

#run matching for second choice
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 2, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
match(True, 2, subj_counts, matches, unmatched, fellows, tutees, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

#run matching for third choice
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 3, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
match(True, 3, subj_counts, matches, unmatched, fellows, tutees, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

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
fields = ['Fellow', 'Fellow Tutee Count', 'Tutee', 'Choice', 'Evaluation', 'Grade', 'Fellow Grades', 'Subject', 'Fellow Subjects', 'Tutee Platform', 'Fellow Platform', 'Tutee Availbility', 'Fellow Availbility']
filename = "matches.csv"

#writing to file
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for fellow, value in matches.items():
        for i in range(1,len(value)):
            # get tutee info
            tutee_match = value[i]
            tutee, choice = tutee_match
            tutee_info = tutees[tutee]
            grade = tutee_info['Grade']
            # get fellow info
            fellow_info = fellows[fellow]
            subject, evaluation = TuteeInfoByChoice(tutee_info, choice)
            if not checkSubject(subject, fellow_info['subjects']):
                print("Matching error: Tutee subject and fellow subject do not match", fellow,tutee)
            if not checkAvailability(tutee_info['Availability'], fellow_info['availability']):
                print("Matching error: Tutee subject and fellow availabilities do not match", fellow,tutee)
            if not checkPlatform(tutee_info['Platform'], fellow_info['platform']):
                print("Matching error: Tutee subject and fellow platforms do not match", fellow,tutee)
            if not checkGrade(grade, fellow_info['grades']):
                print("Matching error: Tutee subject and fellow grades do not match", fellow,tutee)
            row = [fellow, fellow_info['tut_count'], tutee, choice, evaluation, grade, fellow_info['grades'], subject, fellow_info['subjects'], tutee_info['Platform'], fellow_info['platform'], tutee_info['Availability'], fellow_info['availability']]
            csvwriter.writerow(row)

toc = time.perf_counter()
print(f"Script ran in {toc - tic:0.4f} seconds")