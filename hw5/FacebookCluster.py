# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 17:46:52 2014

@author: sthirumalai and eocallaghan
"""


#importing pattern to be used to fetch facebook data
from pattern.web import *
from pattern.en import *
#Lizzy's Facebook liscence
f_lizzie = Facebook(license='CAAEuAis8fUgBAAG8SBjH7bEAimzm6shZBMmOFaginXZCuxdPftGBZBFfHnOYEZAWWBowqHCDzCKNniyeZAm6Feimonnjcgv3hFEG8CLKcbIPHn727Hf9wqPsPV9HNd0V7LHBiN3lUyxWawxmhKbZCtXDjVU6KZBGQ9rLqTgjiHnNvb3CZCkhVzpA36whZB7nRq9EZD')
#Shrinidhi's Facebook liscence
f_shrin = Facebook(license='CAAEuAis8fUgBAGjbDK3oFYhbFCtymaT4emLFUO2gzgarzB5I9aG4G1ZC7lgvAFnKuT47f0qvvSsKlWuUVF5GOffpbDOORJY68ipZATlyBO43o6ZCXWo3vAIOEi3akZAzfqxp2Heydm3ouLVv9zHHfzbRw9tt7CVOR0Y6ZCHNP1nwqDku7nZADn')

def get_posts_string(news_list, name, num):
    """
    Takes input of a list of all posts related to a friend, only filters out statuses,
    and outputs them in one string with all statuses seperated by spaces.
    """
    friend_statuses = '' #initializes string of statuses
    #iterates through all posts
    for news in news_list:
        post = str(news.text) #gets text of each status
        #filters out only posts made by friend
        if (not post.__contains__(name)) and (str(news.author).__contains__(name)):
            #if post is on someone elses wall, filters out only the text posted on wall
            if post.__contains__('"'):
                start = post.index('"')
                end = (post[start:]).index('"')
                post = post[start:end]
            #creates concatinated string of all statuses
            friend_statuses = friend_statuses + ' ' + post
    #print num #debugging helper commented out for the sake of shortening output
    return friend_statuses
    
def get_posts(f): 
    """ 
    1. Goes through all friends of user of inputted facebook liscence
    2. Gets all statuses of each friend and concatinates all statuses into one string
    3. Creates a dictionary with the keys as the facebook friend and the value as the string of statuses
    """
    posts_list = {} #initializes dictionary
    me = f.profile() #gets profile from given liscence
    my_friends = f.search(me[0], type=FRIENDS, count=100)
    tick = 0 #debugging helper
    #iterates through all friends of user
    for friend in my_friends:
        tick = tick + 1 #debugging helper: prints out iteration of friend
        friend_name = str(friend.text)
        #gets all posts related to friend, passes if none are found
        try:
            friend_news = f.search(friend.id, type=NEWS, count =20, timeout = 5)
        except URLTimeout:
            pass
        #creates dictionary of friends with statuses
        posts_list[friend_name] = get_posts_string(friend_news, friend_name, tick)
    return posts_list

def find_sentiments(friends):
    """Takes a dictionary of people and text written by all of the people the Key
    is the person's name and the value the text written by said person in string form
    The function then finds the polarity, or positivity of each person's text and returns it
    in the form of a dictionary with the Keys being person names and the values the positivity.
    The positivity is a number between -1 and 1 where 1 is most positive"""
    friend_sentiment = {}
    for key in friends:
        analyzed_sentiment = sentiment(friends[key])
        friend_sentiment[key] = analyzed_sentiment[0]
        
    return friend_sentiment
    
def find_sentiments_unit_test():
    """Unit test for find_sentiments(dictionary) uses a small dictionary of known subjectivities
    and passes it to find_sentiments"""
    friends = {}
    friends['mostPositive'] = "I'm really excited!!!"
    friends['middle'] = "I'm netural"
    friends['repeat'] = "I'm also neutral"
    friends['mostNegative'] = "I hate life"
    print "Theoretical output (order doesn't matter because using dictionarys) {'most positive': .732421875, 'middle': 0.0, 'repeat': 0.0, 'most negative': -.8}"
    print "Actual output: "
    print find_sentiments(friends)

def find_subjectivity(friends):
    """Takes a dictionary of people and text written by all of the people the Key
    is the person's name and the value the text written by said person in string form
    The function then finds the subjectivity of each person's text and returns it
    in the form of a dictionary with the Keys being person names and the values the subjectivity.
    The positivity is a number between 0 and 1 where 1 is most subjective"""
    
    friend_subjective = {}
    for key in friends:
        analyzed_subjective = sentiment(friends[key])
        friend_subjective[key] = analyzed_subjective[1]
        
    return friend_subjective

def find_subjectivity_unit_test():
    """Unit test for find_subjectivity(dictionary) uses a small dictionary of known subjectivities
    and passes it to find_subjective"""
    friends = {}
    friends['mostSubjective'] = "I think cats are awesome!!!"
    friends['middle'] = "I really like cats."
    friends['repeat'] = "I also really like cats."
    friends['mostObjective'] = "Cats are animals."
    print "Theoretical output (order doesn't matter because using dictionarys) {'mostSubjective': 1.0, 'middle': 0.2, 'repeat': 0.2, 'most Objective': 0.0}"
    print "Actual output: "
    print find_subjectivity(friends)
    
def most_Positive_Person(sentiments):
    """Takes a dictionary of people and positivity (a number between -1 and 1) of the people. The Key
    is the person's name and the value the positivity index. The function then finds the most 
    positive person and returns his or her name as a string."""
    mostPositive = -1;
    mostPositivePerson = ""
    for key in sentiments:
        if sentiments[key]>mostPositive:
            mostPositive = sentiments[key]
            mostPositivePerson = key
    return mostPositivePerson
    
def most_Positive_Person_unit_test():
    """Unit test for most_Positive_Person uses a small dictionary of known sentiments
    and passes it to most_Positive_Person"""
    friends = {}
    friends['mostPositive'] = "I'm really excited!!!"
    friends['middle'] = "I'm netural"
    friends['repeat'] = "I'm also neutral"
    friends['mostNegative'] = "I hate life"
    print "Theoretical output: 'mostPositive"
    print "Actual output: "
    print most_Positive_Person(find_sentiments(friends))
    
def most_Negative_Person(sentiments):
    """Takes a dictionary of people and positivity (a number between -1 and 1) of the people. The Key
    is the person's name and the value the positivity index. The function then finds the most 
    negative person and returns his or her name as a string."""
    mostNegative = 1;
    mostNegativePerson = ""
    for key in sentiments:
        if sentiments[key]<mostNegative:
            mostNegative = sentiments[key]
            mostNegativePerson = key
    return mostNegativePerson
    
def most_Negative_Person_unit_test():
    """Unit test for most_Negative_Person uses a small dictionary of known sentiments
    and passes it to most_Negative_Person"""
    friends = {}
    friends['mostPositive'] = "I'm really excited!!!"
    friends['middle'] = "I'm netural"
    friends['repeat'] = "I'm also neutral"
    friends['mostNegative'] = "I hate life"
    print "Theoretical output: 'mostNegative"
    print "Actual output: "
    print most_Negative_Person(find_sentiments(friends))

    
def sort_sentiments_postive(sentiments):
    """Takes a dictionary of people and positivity (a number between -1 and 1) of the people. The Key
    is the person's name and the value the positivity index. The function then returns a list 
    of people starting with most positive and ending with most negative."""
    positivePeople = []
    for people in sorted(sentiments, key=sentiments.get, reverse=True):
        positivePeople.append(people)
    return positivePeople
    
def sort_sentiments_positive_unit_test():
    """Unit test for sort_sentiments_positive uses a small dictionary of known sentiments
    and passes it to sort_sentiments_positive"""
    friends = {}
    friends['mostPositive'] = "I'm really excited!!!"
    friends['middle'] = "I'm netural"
    friends['repeat'] = "I'm also neutral"
    friends['mostNegative'] = "I hate life"
    sentiments = find_sentiments(friends)
    print "Theoretical output: ['mostPositive', 'middle', 'repeat', 'mostNegative']"
    print "Actual output: "
    print sort_sentiments_postive(sentiments)
        
def sort_sentiments_negative(sentiments):
    """Takes a dictionary of people and positivity (a number between -1 and 1) of the people. The Key
    is the person's name and the value the positivity index The function then returns a list 
    of people starting with most negative and ending with most positive."""
    negativePeople = []
    for people in sorted(sentiments, key=sentiments.get):
        negativePeople.append(people)
 
    return negativePeople
   
def sort_sentiments_negative_unit_test():
    """Unit test for sort_sentiments_negative uses a small dictionary of known sentiments
    and passes it to sort_sentiments_negative"""
    friends = {}
    friends['mostPositive'] = "I'm really excited!!!"
    friends['middle'] = "I'm netural"
    friends['repeat'] = "I'm also neutral"
    friends['mostNegative'] = "I hate life"
    sentiments = find_sentiments(friends)
    print "Theoretical output: ['mostNegative', 'middle', 'repeat', 'mostPositive']"
    print "Actual output: "
    print sort_sentiments_negative(sentiments)
    
def most_subjective(subjectivity):
    """Takes a dictionary of people and subjectivity (a number between 0 and 1) of the people. The Key
    is the person's name and the value the subjectivity index. The function then finds the most 
    subjective person and returns his or her name as a string."""
    mostSubjective = 0;
    mostSubjectivePerson = ""
    for key in subjectivity:
        #print key
        #print subjectivity[key]
        if subjectivity[key] > mostSubjective:
            mostSubjective = subjectivity[key]
            mostSubjectivePerson = key
    return mostSubjectivePerson
    
def most_subjective_unit_test():
    """Unit test for most_subjective uses a small dictionary of known subjectivities
    and passes it to most_subjective"""
    friends = {}
    friends["mostSubjective"] = "I think cats are awesome!!!"
    friends["middle"] = "I really like cats."
    friends["repeat"] = "Ialso really like cats."
    friends["mostObjective"] = "Cats are animals."
    print "Theoretical output: 'mostObjective'"
    print "Actual output: "
    subjectivity = find_subjectivity(friends)
    print most_subjective(subjectivity)
    
def most_objective(subjectivity):
    """Takes a dictionary of people and subjectivity (a number between 0 and 1) of the people. The Key
    is the person's name and the value the subjectivity index. The function then finds the most 
    objective person and returns his or her name as a string."""
    mostObjective = 1;
    mostObjectivePerson = ""
    for key in subjectivity:
        if subjectivity[key]<mostObjective:
            mostObjective = subjectivity[key]
            mostObjectivePerson = key
    return mostObjectivePerson

def most_objective_unit_test():
    """Unit test for most_objective uses a small dictionary of known subjectivities
    and passes it to most_objective"""
    friends = {}
    friends["mostSubjective"] = "I think cats are awesome!!!"
    friends["middle"] = "I really like cats."
    friends["repeat"] = "Ialso really like cats."
    friends["mostObjective"] = "Cats are animals."
    print "Theoretical output: mostObjective"
    print "Actual output: "
    subjectivity = find_subjectivity(friends)
    print most_objective(subjectivity)
    
def sort_subjectivity(subjectivy):
    """Takes a dictionary of people and subjectivity (a number between 0 and 1) of the people. The Key
    is the person's name and the value the subjectivity index. The function then returns a list 
    of people starting with most subjective and ending with most objective."""
    subjectivePeople = []
    for people in sorted(subjectivy, key=subjectivy.get, reverse=True):
        subjectivePeople.append(people)
    return subjectivePeople
    
def sort_subjectivity_unit_test():
    """Unit test for sort_subjectivity uses a small dictionary of known subjectivities
    and passes it to sort_subjectivity"""
    friends = {}
    friends["mostSubjective"] = "I think cats are awesome!!!"
    friends["middle"] = "I really like cats."
    friends["repeat"] = "I also really like cats."
    friends["mostObjective"] = "Cats are animals."
    print "Theoretical output: [mostSubjective, middle, repeat, mustObjective']"
    print "Actual output: "
    subjectivity = find_subjectivity(friends)
    print sort_subjectivity(subjectivity)
       
def sort_objectivity(subjectivy):
    """Takes a dictionary of people and subjectivity (a number between 0 and 1) of the people. The Key
    is the person's name and the value the subjectivity index. The function then returns a list 
    of people starting with most subjective and ending with most objective."""
    objectivePeople = []
    for people in sorted(subjectivy, key=subjectivy.get):
        objectivePeople.append(people)
    return objectivePeople
    
def sort_objectivity_unit_test():
    """Unit test for sort_subjectivity uses a small dictionary of known subjectivities
    and passes it to sort_subjectivity"""
    friends = {}
    friends["mostSubjective"] = "I think cats are awesome!!!"
    friends["middle"] = "I really like cats."
    friends["repeat"] = "Ialso really like cats."
    friends["mostObjective"] = "Cats are animals."
    print "Theoretical output: [mustObjective, middle, repeat,mostSubjective]"
    print "Actual output: "
    subjectivity = find_subjectivity(friends)
    print sort_objectivity(subjectivity)

def main():
    """runs all unit tests and then runs code for FB friends use runUnitTest and runFacebook
    to run all the unit tests and the code that uses facebook respecivily"""
    runUnitTest = False
    runFacebook = True
    if runUnitTest:
        print "UnitTests"
        print "\nfind sentiments unit test: "
        find_sentiments_unit_test()
        print "\nfind subjectivity unit test: "
        find_subjectivity_unit_test()
        print "\nmost positive person unit test: "
        most_Positive_Person_unit_test()
        print "\nmost negative unit test: "
        most_Negative_Person_unit_test()
        print "\nsort sentiments positive unit test: "
        sort_sentiments_positive_unit_test()
        print "\nsort sentiments negative unit test: "
        sort_sentiments_negative_unit_test()
        print "\nmost subjective unit test: "
        most_subjective_unit_test()
        print "\nmost objective unit test: "
        most_objective_unit_test()
        print "\nsort subjectivity unit test: "
        sort_subjectivity_unit_test()     
        print "\nsort objectivity unit test: "
        sort_objectivity_unit_test()
    
    if runFacebook:
        posts = get_posts(f_lizzie)   
        sentimentList = find_sentiments(posts)
        subjectiveList = find_subjectivity(posts)
        print "\n Facebook Code:"
        print "\nmost postive person: "
        print most_Positive_Person(sentimentList)
        print "\nmost negative person: "
        print most_Negative_Person(sentimentList)
        print "\nmost subjective person: "
        print most_subjective(subjectiveList)
        print "\nmost objective person: "
        print most_objective(subjectiveList)
        print "\npeople sorted by most positive: "
        print sort_sentiments_postive(sentimentList)
        print "\npeople sorted by most negative: "
        print sort_sentiments_negative(sentimentList)
        print "\npeople sorted by most subjective: "
        print sort_subjectivity(subjectiveList)
        print "\npeople sorted by most objective: "    
        print sort_objectivity(subjectiveList)