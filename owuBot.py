import praw

##--------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------------------------##

# Strings for matching heroes of interest in post titles
reinStrings = ['Reinhardt', 'reinhardt', 'rein', 'Rein']
orisaStrings = ['Orisa', 'orisa']
winstonStrings = ['Monkey', 'monkey', 'winston', 'Winston']

# Uses ANSI formatting; prints multiple hero categroies to the same line
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

# The guide object representing a given guide or post on the OWU subreddit
class Guide:

	def __init__(self, title, includedHeroes, url):
		self.title = title
		self.includedHeroes = includedHeroes
		self.url = url

	def printGuide(self):
		print('\n')
		print('\x1b[4;35;40m' + '---' + self.title + '---' + '\x1b[0m')
		print('URL: ' + self.url)

	# Category types for the day are stored as a set of tuples, here we check for equality of the guide 
	# object's list of included heroes against those tuples:
	def isInCategory(self, categoryTuple):
		if len(categoryTuple) != len (self.includedHeroes):
			return False

		for category in categoryTuple:
			categoryIsIncluded = False
			for hero in self.includedHeroes:
				if hero == category:
					categoryIsIncluded = True
					break
			if categoryIsIncluded == False:
				return False

		return True

##--------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------------------------##

#Use praw API to interface with reddit and fetch the new posts from reddit.com/overwatchuniversity
reddit = praw.Reddit('bot1', user_agent='<Python:reddyBot:v1.0 (by /u/reddyBootboot)')
newPosts = reddit.subreddit('overwatchuniversity').new()

todaysGuides = []
todaysHeroCombinations = set()

#Iterate through today's new posts, and for each post which mentions one or more of the heroes of interest
#create a guide object for that post and add the hero combination as a category for today's guides:
for submission in newPosts:

	heroesInCurrentSubmission = []

	for reinString in reinStrings:
		if reinString in submission.title:
			heroesInCurrentSubmission.append('Reinhardt')
			break
	for orisaString in orisaStrings:
		if orisaString in submission.title:
			heroesInCurrentSubmission.append('Orisa')
			break
	for winstonString in winstonStrings:
		if winstonString in submission.title:
			heroesInCurrentSubmission.append('Winston')
			break

	if len(heroesInCurrentSubmission) > 0:
		todaysHeroCombinations.add(tuple(heroesInCurrentSubmission))
		todaysGuides.append(Guide(submission.title, heroesInCurrentSubmission, submission.url))

#Output:
print('\x1b[1;35;40m' + 'Today\'s Main-tank guides featured on OWU:\n' + '\x1b[0m')

if len(todaysHeroCombinations) > 0:
	for heroCombination in todaysHeroCombinations:
		printCategoryTitle(heroCombination)
		for guide in todaysGuides:
			if guide.isInCategory(heroCombination):
				guide.printGuide()

##--------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------------------------------------------------##
