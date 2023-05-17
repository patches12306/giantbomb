import requests
import logging
import pandas as pd
from difflib import get_close_matches
import json


#SNES = id 9
#NES = id 21
#N64 = 43
apikey = "2d9d290059ee089eb75febce425705aac20bf43c"

#load data
	#load SNES Data

SNES = []
for i in range(18):	
	added = []
	added=requests.get("https://www.giantbomb.com/api/games/?api_key=2d9d290059ee089eb75febce425705aac20bf43c&format=json&field_list=name,description,site_detail_url,image,aliases&offset="+str(i)+"00&platforms=9", headers={'user-agent':'newcoder'}).json()
	SNES.extend(added['results'])


	#load N64 data
N64 = []
for i in range(4):	
	added = []
	added=requests.get("https://www.giantbomb.com/api/games/?api_key=2d9d290059ee089eb75febce425705aac20bf43c&format=json&field_list=name,description,site_detail_url,image,aliases&offset="+str(i)+"00&platforms=43", headers={'user-agent':'newcoder'}).json()
	N64.extend(added['results'])


NES = []
for i in range(16):	
	added = []
	added=requests.get("https://www.giantbomb.com/api/games/?api_key=2d9d290059ee089eb75febce425705aac20bf43c&format=json&field_list=name,description,site_detail_url,image,aliases&offset="+str(i)+"00&platforms=21", headers={'user-agent':'newcoder'}).json()
	NES.extend(added['results'])

#combine all data
ALL = []
ALL.extend(N64)
ALL.extend(NES)
ALL.extend(SNES)

ALL_df = pd.DataFrame.from_dict(ALL)
ALL_df = ALL_df.set_index('name')


# get list of game names and a list of keywords

# print(rslt_df)

name_list = rslt_df.index.tolist()
similar_arr = []
for i in name_list:
    name_arr = i.split(" ")
    for n in name_arr:
        # print(n)
        if n not in similar_arr:
            similar_arr.append(n)

# function that asks user for keyword input and returns either suggested keywords of dataframe of matched games
def get_game():
    query = ""
    #list of potential conjunctions/words not to capitalize checking for capitalizations
    dont_cap = ["and","in","the","or","is","with","a","as","for","of"]
    #loop to ask users for input
    while query != "quit":
        query = input("Enter query: or enter quit to end ")
        # checks dataframe of all games that see if keyword matches
        rslt_df = ALL_df[ALL_df.index.str.contains(query)]
        # quit if use enters "quit"
        if query == "quit":
            print("Quitting!")
            return
        #tells uers to enter a query if blank input
        elif query =="":
            print("please enter a query")
        #if no keywords match, return list of either similar games or similar keywords to user's input
        elif rslt_df.empty:
            similar_df=get_close_matches(query, similar_arr)
            name_df=get_close_matches(query, name_list)
            if similar_df!=[] or name_df!=[]:
                print("couldn't find your game, did you mean one of these keywords?")
                if similar_df!=[]:
                    print((get_close_matches(query, similar_df)))
                if name_df!=[]:
                    print((get_close_matches(query, name_df)))
        	#if nothing similar could be found, tells user nothing could be find
            else:
                print("couldn't find your game or similar keywords")
            
### code to check for and replace capitalizations, to use comment or remove all code after "elif rslt_df.empty:" and uncomment code below
#             if " " in query:
#                 c_arr = []
#                 q_arr = query.split(" ")
#                 c_arr.append(q_arr[0].capitalize())
#                 for i in q_arr[1:]:
#                     if i in dont_cap:
#                         c_arr.append(i)
#                     else:
#                         c_arr.append(i.capitalize())
#                 query = " ".join(c_arr)
#                 rslt_df = ALL_df[ALL_df.index.str.contains(query)]
#                 print("Results for "+query)
#                 print("Number of rResults: "+ str(len(rslt_df)))
#                 print(rslt_df)
                
#             else:
#                 query = query.capitalize()
#                 rslt_df = ALL_df[ALL_df.index.str.contains(query)]
#                 print("Results for "+query)
#                 print("Number of rResults: "+ str(len(rslt_df)))
#                 print(rslt_df)     
		# prints number results and dataframe of resukts
        else:
            print("Results for "+query)
            print("Number of Results: "+ str(len(rslt_df)))
            print(rslt_df)


get_game()





