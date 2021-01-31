# hatch-matching

Hatch matching algorithm


Matching Algorithm: 


```diff
- text in
-
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
<p class="text-right" style="color:#808080;">


## Hatch Matching API: 
### Fellows Data Parsing 
```diff
Given
+ def addFellow(row)
# Given full row of data for a fellow, sort the fellow into corresponding subject buckets by level of education 

+ def removeFellow(fellow)
Remove given fellow from all subject buckets that contain the fellow 

+ def updateCapacity(fellow, capacity)
Given a fellow and a new tutee capacity update the fellow's capacity for all subject buckets that contains the fellow

+ def makeHeap(heap, gradelist, gradename)
Given a heap, a list of subject buckets containing fellows, and the grade level corresponding to the list
create a minheap 

+ def makeHeap(heap, gradelist, gradename)
Create a minheap of subjects ordered by number of fellows per subject
First item = the subject with least number of fellows

```
### Tutee Data Parsing 
```diff
+ def clearTuteeBuckets(low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee)

+ def TuteeInfoByChoice(info, choice)

+ def makeTuteeBucket(unmatched, choice, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, tutees)

```

### Matching 
```diff
+ def updateSubjectCounts(subj_counts, low_elementary, high_elementary, middle, high)

+ def makeMatch(multiple, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap)

+ def getTuteeInfo(tutee)

+ def getFellowInfo(fellow)

+ def checkMatchCriterea(multiple, tutee_platform, fellow_platform, tutee_availability, fellow_availability, unmatched, tutee, matches, fellow, choice, tut_count, fellow_heap)

+ def matchGrades(multiple, fellow_candidates, tutee_candidates, choice)

+ def match(multiple, choice, subj_counts, unmatched, low_elementary_tutee, high_elementary_tutee, middle_tutee, high_tutee, low_elementary, high_elementary, middle, high)
```
