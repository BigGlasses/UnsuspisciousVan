'''
Created on Feb 25, 2015

@author: Owner
'''
import  pygame, cPickle, thread, time,random
from color import *

story = [None for i in range(30)]

cactus = [2]
shrub = [3]
shrub2 = [4]
hydrant = [1]
debris = []
dumpster = []
tempStory = {}
tempStory['message'] = "Delivery Failed(everyone died)/nStarting over..."
tempStory['foliageSprites'] = []
tempStory['horizonSprites'] = []
tempStory['music'] = 8
tempStory['length'] = 5
tempStory['scrollSky'] = True
tempStory['scrollGround'] = True
tempStory['slidespeed'] = 45
tempStory['specialProj'] = []
tempStory['specialSpawn'] = []
tempStory['skyColor'] = 0
tempStory['groundColor'] = 0
tempStory['ending'] = ""
tempStory['paths'] = [1,4,4,4]
story[0] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Day 1@ You begin your journey to deliver ice cream, but first you must travel through the city."
tempStory['foliageSprites'] = []
tempStory['horizonSprites'] = dumpster
tempStory['length'] = 5
tempStory['specialProj'] = []
tempStory['specialSpawn'] = []
tempStory['slidespeed'] = 15
tempStory['skyColor'] = 1
tempStory['groundColor'] = 0
tempStory['ending'] = ""
tempStory['paths'] = [2,4]
story[1] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Day 2@ Your van is running out of fuel.@ You resolve to collect kittens to fuel your van.@ of course."
tempStory['foliageSprites'] = []
tempStory['horizonSprites'] = hydrant
tempStory['points'] = [0,5]
tempStory['length'] = 30
tempStory['music'] = 3
tempStory['specialProj'] = [0]
tempStory['specialSpawn'] = [4]
tempStory['skyColor'] = 1
tempStory['groundColor'] = 0
tempStory['paths'] = [3]
story[2] = tempStory

tempStory = story[2].copy()
tempStory['message'] = "You have overfarmed the kittens.@ They begin to fight back."
tempStory['length'] = 20
tempStory['specialProj'] = [0,1]
tempStory['specialSpawn'] = [2,2]
tempStory['ending'] = "Your hunger for kittens has been sated."
tempStory['paths'] = [4]
story[3] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Day 6@ Old western bandits have found their way into the city somehow."
tempStory['foliageSprites'] = []
tempStory['horizonSprites'] = hydrant + dumpster
tempStory['length'] = 15
tempStory['specialProj'] = [2]
tempStory['skyColor'] = 1
tempStory['specialSpawn'] = [1]
tempStory['groundColor'] = 0
tempStory['ending'] = ""
tempStory['paths'] = [5]
story[4] = tempStory

tempStory = story[4].copy()
tempStory['message'] = "More bandits arrive to ruin your day."
tempStory['length'] = 30
tempStory['skyColor'] = SANDYELLOW
tempStory['specialSpawn'] = [2]
tempStory['groundColor'] = 0
tempStory['ending'] = ""
tempStory['paths'] = [6]
story[5] = tempStory

tempStory = story[5].copy()
tempStory['message'] = "%s came up with the brilliant idea to drive faster to outrun the bandits."
tempStory['length'] = 30
tempStory['skyColor'] = SANDYELLOW
tempStory['specialProj'] = [2,3]
tempStory['specialSpawn'] = [1,2]
tempStory['slidespeed'] = 80
tempStory['ending'] = "You've outrun the bandits."
tempStory['paths'] = [7]
story[6] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Day 14@ Your journey has finally taken you to the city limits."
tempStory['length'] = 5
tempStory['groundColor'] = BEIGE
tempStory['skyColor'] = 1
tempStory['ending'] = "%s sees something strange off in the distance."
tempStory['paths'] = [8,12,12,12]
story[7] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Whatever it was, it distracted you from the sinkhole you fell down."
tempStory['length'] = 5
tempStory['skyColor'] = BLACK
tempStory['groundColor'] = BLACK
tempStory['ending'] = "%s realizes that is very dark."
tempStory['paths'] = [9]
story[8] = tempStory

tempStory = story[8].copy()
tempStory['message'] = ""
tempStory['length'] = 5
tempStory['ending'] = ""
tempStory['paths'] = [10]
story[9] = tempStory

tempStory = story[9].copy()
tempStory['message'] = "%s turned on a light, awakening an angry ancient crow god, whoops."
tempStory['length'] = 5
tempStory['music'] = 2
tempStory['ending'] = "The angry crow god has been destroyed."
tempStory['skyColor'] = 2
tempStory['groundColor'] = 1
tempStory['specialProj'] = [4]
tempStory['specialSpawn'] = [-1]
tempStory['paths'] = [11]
story[10] = tempStory

tempStory = story[10].copy()
tempStory['message'] = "The ruins are beginning to collapse because they ran out of magic or something."
tempStory['length'] = 20
tempStory['ending'] = "You narrowly escape your demise"
tempStory['skyColor'] = 2
tempStory['slidespeed'] = 90
tempStory['groundColor'] = 1
tempStory['specialProj'] = [5]
tempStory['specialSpawn'] = [4]
tempStory['paths'] = [18]
story[11] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Day 27@ There was a small ocean that you never noticed before."
tempStory['length'] = 5
tempStory['ending'] = ""
tempStory['music'] = 1
tempStory['paths'] = [13]
tempStory['skyColor'] = 3
tempStory['groundColor'] = 2
tempStory['paths'] = [13,25]
story[12] = tempStory

tempStory = story[12].copy()
tempStory['message'] = "The seagulls really wanted your icecream for some reason."
tempStory['length'] = 15
tempStory['ending'] = ""
tempStory['specialProj'] = [6]
tempStory['specialSpawn'] = [6]
tempStory['slidespeed'] = 60
tempStory['paths'] = [14]
story[13] = tempStory

tempStory = story[13].copy()
tempStory['message'] = "The king seagull came to order his loyal subjects."
tempStory['length'] = 5
tempStory['ending'] = "The coup has succeeded."
tempStory['specialProj'] = [7]
tempStory['specialSpawn'] = [-1]
tempStory['slidespeed'] = 60
tempStory['paths'] = [18]
story[14] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "You decide to drive up a building to reach the sky."
tempStory['length'] = 5
tempStory['skyColor'] = 4
tempStory['groundColor'] = 3
tempStory['specialProj'] = []
tempStory['specialSpawn'] = []
tempStory['music'] = 7
tempStory['paths'] = [16]
story[15] = tempStory

tempStory = story[15].copy()
tempStory['message'] = "Spiders seem to be after your icecream too. Giant spiders."
tempStory['length'] = 20
tempStory['specialProj'] = [8]
tempStory['specialSpawn'] = [2]
tempStory['paths'] = [17]
story[16] = tempStory

tempStory = story[16].copy()
tempStory['message'] = "The bandits have teamed up with the spiders to take you down."
tempStory['length'] = 30
tempStory['specialProj'] = [8,2]
tempStory['specialSpawn'] = [2,2]
tempStory['ending'] = "%s activates your warp drive."
tempStory['paths'] = [19]
story[17] = tempStory

tempStory = story[7].copy()
tempStory['message'] = "Day 30@ Your journey has finally taken you to the city limits. Again."
tempStory['length'] = 5
tempStory['paths'] = [15]
story[18] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "Day 35@You manage to leave the atmosphere./nYou are almost finished your delivery."
tempStory['length'] = 5
tempStory['skyColor'] = BLACK
tempStory['groundColor'] = 4
tempStory['specialProj'] = []
tempStory['specialSpawn'] = []
tempStory['music'] = 6
tempStory['paths'] = [20]
story[19] = tempStory

tempStory = story[19].copy()
tempStory['message'] = "Just in time, space kittens come to refuel your van."
tempStory['length'] = 20
tempStory['specialProj'] = [9]
tempStory['specialSpawn'] = [2]
tempStory['music'] = 6
tempStory['paths'] = [21]
story[20] = tempStory


tempStory = story[19].copy()
tempStory['message'] = "You must fight off space pirates while you activate your worbaling flanges."
tempStory['length'] = 20
tempStory['specialProj'] = [10]
tempStory['specialSpawn'] = [2]
tempStory['slidespeed'] = 60
tempStory['music'] = 6
tempStory['paths'] = [27]
story[21] = tempStory

tempStory = story[19].copy()
tempStory['message'] = "Day 57@ You are in position to drop to the final destination."
tempStory['length'] = 5
tempStory['slidespeed'] = 15
tempStory['music'] = 6
tempStory['paths'] = [23]
story[22] = tempStory

tempStory = story[0].copy()
tempStory['message'] = "You begin your descent./nKittens, burning in the atmosphere, fell down too."
tempStory['length'] = 5
tempStory['skyColor'] = 4
tempStory['groundColor'] = 5
tempStory['specialProj'] = [12]
tempStory['specialSpawn'] = [2]
tempStory['music'] = 9
tempStory['paths'] = [24]
story[23] = tempStory

tempStory = story[23].copy()
tempStory['message'] = "The FBI arrives to stop you."
tempStory['length'] = 5
tempStory['skyColor'] = 4
tempStory['groundColor'] = 5
tempStory['specialProj'] = [12,11]
tempStory['specialSpawn'] = [2,-1]
tempStory['music'] = 9
tempStory['ending'] = "You defeated the FBI."
tempStory['paths'] = [26]
story[24] = tempStory

tempStory = story[12].copy()
tempStory['message'] = "The pirates heard about %s from their bandit friends."
tempStory['length'] = 30
tempStory['ending'] = ""
tempStory['specialProj'] = [10]
tempStory['specialSpawn'] = [4]
tempStory['paths'] = [13]
story[25] = tempStory

tempStory = story[1].copy()
tempStory['message'] = "You made it."
tempStory['length'] = 10
tempStory['specialProj'] = []
tempStory['specialSpawn'] = []
tempStory['music'] = 4
tempStory['slidespeed'] = 15
tempStory['ending'] = "Congratulations, you have made your delivery."
tempStory['paths'] = [0]
story[26] = tempStory

tempStory = story[19].copy()
tempStory['message'] = "You have attracted a space dragon."
tempStory['length'] = 5
tempStory['specialProj'] = [13]
tempStory['specialSpawn'] = [-1]
tempStory['slidespeed'] = 15
tempStory['ending'] = "Congratulations, you killed an innocent dragon,@ you monster."
tempStory['paths'] = [22]
story[27] = tempStory
