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


# Hatch Matching API: 
## Fellows Data Parsing 
```diff
+ def addFellow(row)
Given full row of data for a fellow, sort the fellow into corresponding subject buckets by level of education 

+ def removeFellow(fellow)
Remove given fellow from all subject buckets that contain the fellow 

+ def updateCapacity(fellow, capacity)
Given a fellow and a new tutee capacity update the fellow's capacity for all subject buckets that contains the fellow

```
2) Tutee Data Parsing 

3) Matching 
