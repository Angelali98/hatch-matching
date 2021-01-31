# hatch-matching

## Matching Algorithm: 


```diff
- Given information: 
-      TUTEE CSV
-           Each row contains data for one tutee including 
-                  Name, Grade in school, Platforms for tutoring, 
-                  Weekly Availability, First Choice Subject, 
-                  Evaluation for first choice subject, Second Choice Subject, 
-                  Evaluation for second choice, Third Choice Subject, Evaluation for Third Choice 
-      FELLOW CSV 
-           Each row contains data for one fellow including 
-                  Name, Grade levels willing to tutor, 
-                  Platforms for tutoring, Weekly Availability, Subjects for tutoring


! 1) Parse the FELLOW CSV. 
!         Create dictionaries for each grade level: lower elementary, high elementary, middle, and high. 
!                 Each dictionary contains keys that are the names of subjects. 
!                 The value per each key is a set of fellows that can tutor the subject.
!         For each fellow in the CSV, add the fellow Name to all subjects that they can tutor in each dictionary.
!
! 2) Create a minheap.  
!         Items in minheap are gradelevel-subjects (i.e. lower-elementary-english)
!         The minheap is ordered by the number of fellows available to tutor that particular subject. 
!         First item in heap is the subject with least number of fellows available. 
!
! 3) Parse the TUTEE CSV. 
!         Create dictionaries for each grade level: lower elementary, high elementary, middle, and high. 
!                 Each dictionary contains keys that are the names of subjects. 
!                 The value per each key is a list of tutees that requested help for that subject.
!         At the beginning of each matching process, a first, second, or third choice of subject is specified.
!
! 4) Perform the matching for non-multiples and first choice subject.
!         Non-multiples means that the algorithm attempts to assign one tutee to each fellow. 
!         Iterate through the minheap created in step 2.
!         Per each subject popped from the minheap, attempt to create tutee-fellow pairings based on the following criterea:
!                 The availability and platform for the fellow and tutee must match 
!                 The fellows with the largest capacities are matched to the tutees with the lowest evaluation scores 
@
! 5) Perform the matching allowing multiple tutees per a fellow for first, second, third choice subject
!
! 6) Write the tutee-fellow pairings result to a new csv file 

@@ TO-DO: Edge Cases and Unit Tests @@
```


## Hatch Matching API: 
### Fellows Data Parsing 
```diff
+ def addFellow(row)
Given full row of data for a fellow, sort the fellow into corresponding subject buckets by level of education 

+ def removeFellow(fellow)
Remove given fellow from all subject buckets that contain the fellow 

+ def updateCapacity(fellow, capacity)
Given a fellow and a new tutee capacity update the fellow's capacity for all subject buckets that contains the fellow

+ def makeHeap(heap, gradelist, gradename)
Given a heap, a list of subject buckets containing fellows, and the grade level corresponding to the list
create a minheap of subjects ordered by number of fellows per subject
First item = the subject with least number of fellows

```
### Tutee Data Parsing 
```diff
+ def clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)
Given the dictionaries representing each tutee grade level, clear out (empty list) the subject buckets within every grade level

+ def TuteeInfoByChoice(info, choice)
Given the row that contains all the information for a tutee and the number choice of subject (out of first choice, second, third) 
output the subject and evaluation score for that subject

+ def makeTuteeBucket(unmatched, choice, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)
Given the set of unmatched tutees, put them into the proper subject level buckets by grade level 
Insert a tuple = the evaluation for the subject with tutee name

```

### Matching 
```diff
+ def updateSubjectCounts(subj_counts, low_elementary, high_elementary, middle, high)
Given the dictionaries representing fellows grouped by grade level 
Update the minheap which tracks the number of fellows available per subject 

+ def makeMatch(multiple, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap)
Called by checkMatchCriterea 
Perform the necessary actions per each tutee and fellow when they are paired: 
1. Remove tutee from unmatched list
2. Update the tutee capacity for the fellow
3. If the fellow capacity reaches zero, remove the fellow from all subject buckets 
4. If the fellow capacity is not zero, then put the fellow back into the candidates if MULTIPLE tutees per fellow is allowed  
5. Add the fellow-tutee pair to the matches 

+ def getTuteeInfo(tutee)
Given a tutee name return the platform and availability of tutee

+ def getFellowInfo(fellow)
Given a fellow name return the platform and availability of fellow

+ def checkMatchCriterea(multiple, tutee_platform, fellow_platform, tutee_availability, fellow_availability, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap)
 Called by matchGrades
 For the given fellow and tutee check if the platform and availability match between a tutee and fellow

+ def matchGrades(multiple, fellow_candidates, tutee_candidates, choice)
Called by the main match function 
Given a list of fellows and list of tutees per a specific subject-gradelevel and the number choice (first, second, or third)
Tterate through the list of tutees and fellow candidates to find matches

+ def match(multiple, choice, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)
Creates matched for tutee-fellow pairs given dictionaries containing tutees and fellows per each grade level. 
Perform matching by the subjecs with the smallest amount of fellow capacity first
Tutees with the lowest subject evaluation scores are matched to the fellows with the highest capacity
```
