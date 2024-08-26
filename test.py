def SearchingChallenge(strArr):
  # get all the keys
  keys = list(set([key[0] for key in strArr])) # list of unique keys
  # create a dictonary of keys
  dict_keys = dict.fromkeys(keys,0)
  #loop over the strArr and get values
  for key in strArr:
    dict_keys[key[0]] += int(key[2:])
  #remove value ==0
  dict_keys = [f"{key}"+":"+f"{value}" for key,value in dict_keys.items() if value != 0]
  
  strArr = [item for item in ]

  # code goes here
  return strArr

# keep this function call here 

print(SearchingChallenge(["X:-1", "Y:1", "X:-4", "B:3", "X:5"]))