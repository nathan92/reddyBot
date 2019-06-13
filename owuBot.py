import praw

reddit = praw.Reddit('bot1', user_agent='<Python:reddyBot:v1.0 (by /u/reddyBootboot)')

reinRefs = ['Reinhardt', 'reinhardt', 'rein', 'Rein']
reinGuides = []

orisaRefs = ['Orisa', 'orisa']
orisaGuides = []

winstonRefs = ['Monkey', 'monkey', 'winston', 'Winston']
winstonGuides = []

newPosts = reddit.subreddit('overwatchuniversity').new()

for submission in newPosts:
	for reinPost in reinRefs:
		if reinPost in submission.title and submission not in reinGuides:
			reinGuides.append(submission)
	for orisaPost in orisaRefs:
		if orisaPost in submission.title and submission not in orisaGuides:
			orisaGuides.append(submission)
	for winstonPost in winstonRefs:
		if winstonPost in submission.title and submission not in winstonGuides:
			winstonGuides.append(submission)

for guide in reinGuides:
	print(guide.title + '\n')
	print(guide.url)

for guide in orisaGuides:
	print(guide.title + '\n')
	print(guide.url)

for guide in winstonGuides:
	print(guide.title + '\n')
	print(guide.url)