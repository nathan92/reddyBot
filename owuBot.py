##--------------------------------------------------------------------------------------------------------##
##----------------------------------------Imports, definitions--------------------------------------------##
##--------------------------------------------------------------------------------------------------------##

import praw
from owuStrings import *

##--------------------------------------------------------------------------------------------------------##
##-------------------------------------------Classes/Functions--------------------------------------------##
##--------------------------------------------------------------------------------------------------------##

# The guide class represents a given guide or post on the OWU subreddit
class Guide:

	def __init__(self, title, includedHeroes, url):
		self.title = title
		self.includedHeroes = tuple(includedHeroes)
		self.url = url

	def printGuide(self):
		print('\n')
		print('\x1b[4;35;40m' + '---' + self.title + '---' + '\x1b[0m')
		print('URL: ' + self.url)

	def isInCategory(self, categoryTuple):
		return categoryTuple == self.includedHeroes

# Gets user input and uses that to define the matching string lists
# For ease of use heroes are divided into 3 pre-set categories
def getUserHeroesFromInput():

	matchingStringLists = []
	try:
		userInput = int(input("Preset number: "))
	except:
		userInput = 0

	if userInput > 3 or userInput < 1:
		print("Invalid selection, defaulting to 1")
		matchingStringLists.extend([reinStrings, orisaStrings, winstonStrings])
		return matchingStringLists

	if userInput == 1:
		# Main tanks: Rein, Orisa, Winston
		matchingStringLists.extend([reinStrings, orisaStrings, winstonStrings])
	elif userInput == 2:
		# Healers: Mercy, Zen, Ana
		matchingStringLists.extend([mercyStrings, anaStrings, zenStrings])
	elif userInput == 3: 
		# DPS: Soldier, Symmetra
		matchingStringLists.extend([soldierStrings, symmetraStrings])
	return matchingStringLists

# Uses ANSI formatting; prints compound hero categroies to the same line
def printCategoryTitle(heroes):

	print('\n' + '\x1b[1;35;40m')
	if len(heroes) > 1:
		for index, hero in enumerate(heroes):
			if index == len(heroes) - 1:
				print(hero, end=' ')
			else:
				print(hero + ' / ', end=' ')
	else:
		print('\x1b[1;35;40m' + heroes[0], end=' ')
	print('guides: ' + '\x1b[0m' + '\n')

def printGenericTitle(titleString):
	print('\x1b[1;35;40m' + titleString + '\n' + '\x1b[0m')

def displayProgramTitle():
	printGenericTitle("OWU scraper")
	print("-----------")
	print("Please select hero preset:")
	print("1) Main tanks: Rein, Orisa, Winston")
	print("2) Healers: Mercy, Zen, Ana")
	print("3) DPS: Soldier, Symmetra")
	print("-----------")


##--------------------------------------------------------------------------------------------------------##
##------------------------------------------Functionality-------------------------------------------------##
##--------------------------------------------------------------------------------------------------------##

displayProgramTitle()

# Use praw API to interface with reddit and fetch the new posts from reddit.com/overwatchuniversity
reddit = praw.Reddit('bot1', user_agent='<Python:reddyBot:v1.0 (by /u/reddyBootboot)')
newPosts = reddit.subreddit('overwatchuniversity').new()

heroStringLists = getUserHeroesFromInput()

todaysGuides = []
todaysHeroCombinations = set()

# Iterate through today's new posts, and for each post which mentions one or more of the heroes of interest
# create a guide object for that post and add the hero combination as a category for today's guides:
for submission in newPosts:

	heroesInCurrentSubmission = []

	for heroStringList in heroStringLists:
		for heroString in heroStringList:
			if heroString.lower() in submission.title.lower():
				heroesInCurrentSubmission.append(heroStringList[0])
				break

	if len(heroesInCurrentSubmission) > 0:
		todaysHeroCombinations.add(tuple(heroesInCurrentSubmission))
		todaysGuides.append(Guide(submission.title, heroesInCurrentSubmission, submission.url))

# Output:
if len(todaysHeroCombinations) > 0:
	printGenericTitle('Today\'s relevant guides featured on OWU:')

	for heroCombination in todaysHeroCombinations:
		printCategoryTitle(heroCombination)
		for guide in todaysGuides:
			if guide.isInCategory(heroCombination):
				guide.printGuide()
else:
	printGenericTitle('Sorry, nothing today')


##--------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------------------------##
