import xml.etree.ElementTree as ET
import time
from diff_match_patch import diff_match_patch
import os

tree = ET.parse('The_Weeknd.knolml')
root = tree.getroot()
revisions=[]
for instance in root.iter('Instance'):
  for text in instance.iter('Text'):
    revisions.append(text.text)

def diff_match(text1,text2):
  dmp = diff_match_patch()
  start = time.time()
  diff = dmp.patch_make(text1,text2)
  diff = dmp.patch_toText(diff)
  end = time.time()
  return (end-start) , diff

def patch_match(text1,diff):
  dmp = diff_match_patch()
  start = time.time()
  patches = dmp.patch_fromText(diff)
  new_text, _ = dmp.patch_apply(patches, text1)
  end = time.time()
  return (end-start),new_text

print(len(revisions))

temp1 = time.time()
temp2 = time.time()
temptime =  temp2-temp1
diff_time_k=[]
patch_time_k = []
file_size_k = []
val = 86;                              #########################################################################  update k value here

for k in range(val,val+1,1):
  diff_list = []
  diff_time = []
  patch_time = []
  patch_list = []
  patch_files = []
  for i in range(len(revisions)):
    if (i%k==0):
      diff_list.append(revisions[i])
      diff_time.append(temptime)
    else :
      temp = int(i/k)
      prev_text = revisions[k*temp]
      cur_text= revisions[i]
      t , diff = diff_match(prev_text,cur_text)
      diff_list.append(diff)
      diff_time.append(t)
  for i in range(len(revisions)):
    if i%k==0:
      temp = int(i/k)
      current_text = diff_list[k*temp]
      patch_time.append(temptime)
      patch_files.append(current_text)
    else:
      temp = int(i/k)
      patched_text = diff_list[k*temp]
      total = 0
      t,patched_text = patch_match(patched_text,diff_list[i])
      total+=t
      patch_time.append(total)
      patch_files.append(patched_text)

  total_time_diff=0
  total_time_patch=0
  l = ""
  for i in range(len(diff_time)):
    total_time_diff +=diff_time[i]
    total_time_patch +=patch_time[i]
    l+=diff_list[i]
  diff_time_k.append(total_time_diff)
  patch_time_k.append(total_time_patch)
  file_size_k.append(len(l.encode('utf-8')))

print ("k","diff_time      ","patch_time   ","total_time","all_file_size")
print("sqrt(n)",diff_time_k[0],patch_time_k[0],diff_time_k[0]+patch_time_k[0],file_size_k[0])