import requests
from bs4 import BeautifulSoup

def gather_data_table():
	r=requests.get('http://pokemondb.net/type')
	if r.status_code!=200:
		print "Could not connect to server"
		type_database=None
	else:
		page_info=BeautifulSoup(r._content,'html.parser')
		website_type_list=page_info.find_all('a', class_='type-abbr')
		type_list=[]
		type_database={}
		for i in range(0,len(website_type_list)):
			type_list.append(website_type_list[i]['title'])
			type_database[website_type_list[i]['title']]={}
		for i in type_list:
			for j in type_list:
				type_database[i][j]=None	
		website_type_table=page_info.find_all('td', class_='type-fx-cell')
		for i in range(0,len(website_type_table)):
			attacker_type=website_type_table[i]['title'].split('=')[0].split(' ')[0]
			defender_type=website_type_table[i]['title'].split('=')[0].split(' ')[2]
			effect=website_type_table[i]['title'].split('=')[1].strip()
			effect_number=None
			if effect=="super-effective":
				effect_number=2
			if effect=="normal effectiveness":
				effect_number=1
			if effect=="not very effective":
				effect_number=0.5
			if effect=="no effect":
				effect_number=0
			type_database[attacker_type][defender_type]=effect_number
	return type_database

def battle(type_database):
	types=type_database.keys()
	attack_high_score=['type',-999]
	single_type_attack_high_score=['type',-999]
	defense_high_score=['type',-999]
	single_type_defense_high_score=['type',-999]
	defense_score={}
	offense_score={}
	single_type_offense_score={}
	for i in types:
		offense_score[i]=0
		single_type_offense_score[i]=0
#"i" is the defender's 1st type, "j" is the defender's 2nd type, "k" is the type of attack
	for i in types:
		defen	se_score[i]={}
		for j in types:
			defense_score[i][j]=0
			relative_defensive_weight=1
			for k in types:
				relative_offensive_weight=1
				defense_score[i][j]-=relative_offensive_weight*(type_database[k][i]+type_database[k][j])/2
				offense_score[k]+=relative_defensive_weight*(type_database[k][i]+type_database[k][j])/2
				if i==j:
					single_type_offense_score[k]+=relative_defensive_weight*(type_database[k][i]+type_database[k][j])/2
			if defense_score[i][j]>defense_high_score[1]:
				defense_high_score[1]=defense_score[i][j]
				defense_high_score[0]=i+j
			if i==j:
				if defense_score[i][j]>single_type_defense_high_score[1]:
					single_type_defense_high_score[1]=defense_score[i][j]
					single_type_defense_high_score[0]=i
	for k in types:
		if offense_score[k]>attack_high_score[1]:
			attack_high_score[1]=offense_score[k]
			attack_high_score[0]=k
		if single_type_offense_score[k]>single_type_attack_high_score[1]:
			single_type_attack_high_score[1]=single_type_offense_score[k]
			single_type_attack_high_score[0]=k
	return [single_type_attack_high_score, single_type_defense_high_score, attack_high_score, defense_high_score, offense_score, defense_score]

