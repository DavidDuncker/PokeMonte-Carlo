import requests as requestHTTP
from bs4 import BeautifulSoup as HTMLparser

def gatherDataOnPokemonTypes():
	httpRequestForData=requestHTTP.get('http://pokemondb.net/type')
	if httpRequest.status_code!=200:
		print "Could not connect to server"
		dictionaryOfPokemonTypesAndEffectiveness=None
	else:
		parsedHTML=HTMLparser(r._content,'html.parser')
		HTMLparsedListOfPokemonTypes=parsedHTML.find_all('a', class_='type-abbr')
		cleanListOfPokemonTypes=[]
		dictionaryOfPokemonTypesAndEffectiveness={}
		for iterator in range(0,len(HTMLparsedListOfPokemonTypes)):
			currentPokemonType=HTMLparsedListOfPokemonTypes[iterator]['title']
			cleanListOfPokemonTypes.append(currentPokemonType)
			dictionaryOfPokemonTypesAndEffectiveness[currentPokemonType]={}
		for firstIterationOfPokemonTypes in cleanListOfPokemonTypes:
			for secondIterationOfPokemonTypes in cleanListOfPokemonTypes:
				dictionaryOfPokemonTypesAndEffectiveness[firstIterationOfPokemonTypes][secondIterationOfPokemonTypes]=None	
		HTMLparsedListOfPokemonStrengthsAndWeaknesses=parsedHTML.find_all('td', class_='type-fx-cell')
		for i in range(0,len(HTMLparsedListOfPokemonStrengthsAndWeaknesses)):
			typeOfAttacker=HTMLparsedListOfPokemonStrengthsAndWeaknesses[i]['title'].split('=')[0].split(' ')[0]
			typeOfDefender=HTMLparsedListOfPokemonStrengthsAndWeaknesses[i]['title'].split('=')[0].split(' ')[2]
			effectivenessOfAttack=HTMLparsedListOfPokemonStrengthsAndWeaknesses[i]['title'].split('=')[1].strip()
			quantitativeEffectivenessOfAttack=None
			if effectivenessOfAttack=="super-effective":
				quantitativeEffectivenessOfAttack=2
			if effectivenessOfAttack=="normal effectiveness":
				quantitativeEffectivenessOfAttack=1
			if effectivenessOfAttack=="not very effective":
				quantitativeEffectivenessOfAttack=0.5
			if effectivenessOfAttack=="no effect":
				quantitativeEffectivenessOfAttack=0
			dictionaryOfPokemonTypesAndEffectiveness[typeOfAttacker][typeOfDefender]=quantitativeEffectivenessOfAttack
	return dictionaryOfPokemonTypesAndEffectiveness

def simulateBattleWithAllDifferentTypesOfPokemon(dictionaryOfPokemonTypesAndEffectiveness):
	listOfPokemonTypes=dictionaryOfPokemonTypesAndEffectiveness.keys()
	highestScoringAttackerType=['type',-999]
	highestScoringSingleTypeAttacker=['type',-999]
	highestScoringDefenderType=['type',-999]
	highestScoringSingleTypeDefender=['type',-999]
	defenseScoreOfAllPokemonTypes={}
	offenseScoreOfAllPokemonTypes={}
	for i in listOfPokemonTypes:
		offenseScoreOfAllPokemonTypes[i]=0
		defenseScoreOfAllPokemonTypes[i]=0
	for firstDefendingPokemonType in listOfPokemonTypes:
		defenseScoreOfAllPokemonTypes[firstDefendingPokemonType]={}
		for secondDefendingPokemonType in listOfPokemonTypes:
			defenseScoreOfAllPokemonTypes[firstDefendingPokemonType][secondDefendingPokemonType]=0
			relativeAbundanceOfDefensiveType=1
			for attackingPokemonType in listOfPokemonTypes:
				relativeAbundanceOfOffensiveType=1
				defenseScoreOfAllPokemonTypes[i][j] -= relativeAbundanceOfOffensiveType*(dictionaryOfPokemonTypesAndEffectiveness[attackingPokemonType][firstDefendingPokemonType]+dictionaryOfPokemonTypesAndEffectiveness[attackingPokemonType][secondDefendingPokemonType])/2
				offenseScoreOfAllPokemonTypes[k]+=relativeAbundanceOfDefensiveType*(dictionaryOfPokemonTypesAndEffectiveness[attackingPokemonType][firstDefendingPokemonType]+dictionaryOfPokemonTypesAndEffectiveness[attackingPokemonType][secondDefendingPokemonType])/2
			if defenseScoreOfAllPokemonTypes[firstDefendingPokemonType][secondDefendingPokemonType]>highestScoringDefenderType[1]:
				highestScoringDefenderType[1]=defenseScoreOfAllPokemonTypes[firstDefendingPokemonType][secondDefendingPokemonType]
				highestScoringDefenderType[0]=firstDefendingPokemonType+" "+secondDefendingPokemonType
			if firstDefendingPokemonType==secondDefendingPokemonType:
				if defenseScoreOfAllPokemonTypes[firstDefendingPokemonType][secondDefendingPokemonType]>highestScoringSingleTypeDefender[1]:
					highestScoringSingleTypeDefender[1]=defenseScoreOfAllPokemonTypes[firstDefendingPokemonType][secondDefendingPokemonType]
					highestScoringSingleTypeDefender[0]=firstDefendingPokemonType
	for attackingPokemonType in listOfPokemonTypes:
		if offenseScore[attackingPokemonType]>highestScoringAttackerType[1]:
			highestScoringAttackerType[1]=offense_score[attackingPokemonType]
			highestScoringAttackerType[0]=attackingPokemonType

	return [offenseScoreOfAllPokemonTypes,defenseScoreOfAllPokemonTypes,highestScoringAttackerType,highestScoringDefenderType]
