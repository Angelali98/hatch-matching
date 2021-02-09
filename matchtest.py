from matchingfunctions import *

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
clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
unmatched_list = makeTuteeBucket(unmatched, 1, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
print("BREAK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
match(False, 1, subj_counts, matches, unmatched, fellows, tutees, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)

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