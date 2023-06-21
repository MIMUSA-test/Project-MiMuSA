"""Sentiment Explorer module of functions for lexicon based sentiment analysis
model specifically in the Singapore's transport context.

"""
#Libraries to import
import pandas as pd
import nltk
from nltk import word_tokenize
import re
import csv
nltk.download('averaged_perceptron_tagger')

# Read CSV file
replace_words_dic = {}
with open('ngram_20170222_ZX2021_replace_words.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        original_phrase = row['original_phases'].lower()
        target_word1 = row['target_produced_words1'].lower()
        target_word2 = row['target_produced_words2'].lower()
        replace_words_dic[original_phrase] = (target_word1, target_word2)


## All imported dictionaries/databases
profwang_standard_el = pd.read_csv('profwang_standardEL_ONLY.csv')
profwang_singlish = pd.read_csv('profwang_singlish_ONLY.csv')
combined_standard_el = pd.read_csv('profwang&our_standardEL.csv')
combined_singlish = pd.read_csv('profwang&our_singlish.csv')
domaindict = pd.read_csv('transport_dict.csv')

negation_list = ["aren\'t",	"arenot",	"arent",	"can\'t",	"can't", "canot",	"cannot",	"cannt",	"cant",	"coudnt",	"could have",	"couldn\'t",	"couldn't",	"couldnot",	"couldnt",
                "didn\'t",	"didn't",	"didnot",	"didnt",	"doesn\'t",	"doesn't",	"doesnot",	"doesnt",	"don",	"don\'t",	"don't",	"donot",	"dont",	"dosnt", "dun",	"hadn\'t", "weren\'t",
                "hadn't",	"hadnot",	"hadnt",	"hasn\'t",	"hasn't",	"hasnot",	"hasnt",	"haven\'t",	"haven't",	"havenot",	"havent",	"isn\'t",	"isnot", "willnot", "willnt", "willnt",
			    "lack",	"lacked",	"lacking",	"lacks",	"limit",	"limited",	"must\'nt",	"must'nt",	"mustn\'t",	"mustn't",	"mustnot",	"mustnt",	"nednt",	"need\'nt",	"need'nt",	"needn\'t",
                "needn't",	"neednot",	"neednt",	"neither",	"never",	"no",	"nor",	"not",	"ought\'nt",	"ought'nt",	"oughtn\'t",	"oughtn't",	"oughtnot",	"oughtnt",	"rare", "isnt",
                "rarely",	"shan\'t",	"shan't",	"shanot", "shant",	"should have",	"should\'nt",	"should'nt",	"shouldn\'t",	"shouldn't",	"shouldnot",	"shouldnt",	"wasn\'t",	"wasnot",	"wasnt",	
                "werenot",	"werent",	"won\'t",	"won't",	"wont",	"wouldn\'t",	"wouldn't",	"wouldnot",	"wouldnt"]      

negateNeutral = pd.read_csv('negateneutral.csv', header = None)
domainlist = list(domaindict["Word"])
after_adverse = ['but', 'nevertheless', 'even so','yet','no matter what', 'however']
before_adverse = ['even though', 'despite', 'although', 'in spite', 'in spite of the fact that', 'notwithstanding']
multi_data = pd.read_csv('multi-lvl database.v1.1.csv')
A = list(multi_data['A'][:114])
B = list(multi_data['B'])
D = list(multi_data['D'][:-1])   #-1 to remove the NaN value
emojilabels_data = pd.read_csv('emojidb.csv')
emoji_dict = dict(zip((x.encode().decode('unicode_escape') for x in emojilabels_data['Emoji']), emojilabels_data.SentimentNum))
emoji_list = [x.encode().decode('unicode_escape') for x in emojilabels_data.Emoji.values]

def pdColumn_to_list_converter(df):
    """General function to convert df column to list

    """
    df_list = df.values.tolist() #produces list of lists
    proper_list = [item for sublist in df_list for item in sublist] #a single list
    return proper_list


##----------------------------------------------- Step 0 cleaning of text -----------------------------------------------##
def newtext(text):
    
    text = text.strip()
    text = text.replace('/\s\s+/g', ' ') # replace multiple spaces with a single space
    text = text.replace(":)","happy")
    text = text.replace(":(","sad")
    text = re.sub ('\s+', ' ', text)
    text = re.sub('@[^\s]+','',text)  # delete the username
    text = re.sub('&[^\s]+','',text)
    text = re.sub('#[^\s]+','',text)
    text = re.sub('".*?"', '', text)  # delete anything in quotation marks
    text = re.sub('http[s]?://\S+', '', text) # delete urls
    for k, v in replace_words_dic.items():
        if k in text:
            text = re.sub(k,v,text)
    text = text.replace("comfort delgro","comfortdelgro")            
    text = text.replace("as well as","and")
    text = text.replace("as well","also")
    text = text.replace("would like","shall")
    text = text.replace("should have","slightly negative")
    text = text.replace("could have","slightly negative")
    text = text.replace("would have","slightly negative")
    text = text.replace("would be","slightly negative")
    text = text.replace("could be","slightly negative")
    text = text.replace("should be","slightly negative")
    
    text = text.replace("n't","not")
    text = text.replace("n't","not")
    text = text.replace("don","not")
    text = text.replace("dun","not")
    text = text.replace("'s","is")
    text = text.replace("'s","is")
    text = text.replace("'ve","have")
    text = text.replace("'ve","have")
    text = text.replace("'d","had")
    text = text.replace("'d","had")
    text = text.replace("'ll","will")
    text = text.replace("'ll","will")
    text = text.replace("'re","are")
    text = text.replace("'re","are")
    text = text.replace("'m","am")
    text = text.replace("'m","am")

    text = text.replace("should improve","slightly negative")
    text = text.replace("would improve","slightly negative")
    text = text.replace("could improve","slightly negative")
    text = text.replace("would enhance","slightly negative")
    text = text.replace("could enhance","slightly negative")
    text = text.replace("would enhance","slightly negative")
    text = text.replace("to be honest","I will say")
    text = text.replace("it's like","alike")
    text = text.replace("middle finger","slightly negative")
    text = text.replace("snapped","slightly negative")
    text = text.replace("constantly accelerate","slightly negative") 
    text = text.replace("accelerate constantly","slightly negative")
    text = text.replace("accelerate and decelerate constantly","slightly negative") 
    text = text.replace("stopage","negative")
    text = text.replace("constantly accelerate and decelerate","slightly negative") 
    text = text.replace("extension service","good")
    text = text.replace("take advantage","slightly negative")
    text = text.replace("took advantage","slightly negative")
    text = text.replace("taking advantage","slightly negative")
    text = text.replace("takes advantage","slightly negative") 
    #text = text.replace("please help","slightly negative")
    #text = text.replace("please","do") 

    text = re.sub("\S*@\S*\s?",'',text)   # delete email address
    text = text.replace('\n', ' ').replace('\r', '')  # Clean up all "\n"
    
    text = re.sub(r"""
               [)(@#&$]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               "",          # and replace it with no space   [,.;@#?!&$]+ 
               text, flags=re.VERBOSE)
    
    text = text.replace('.', ' .') #specially added to maintain fullstop
    text = text.replace('?', ' ?') #specially added to maintain question mark
    text = text.replace('!', ' !') #specially added to maintain exclamation mark
    text = text.replace(',', ' ,') #specially added to maintain exclamation mark
    text = text.replace(';', ' ;') #specially added to maintain exclamation mark
    text = text.replace(':', ' :') #specially added to maintain exclamation mark
    
    text= re.sub(' +', ' ', text)
    #text= re.sub(':', '', text)
    text= re.sub("[:']", '', text)
    #text = re.sub ('\s+', '', text)
    return text.lower()

def newtext_fullstop(text):
    text = text.strip()
    text = text.replace('/\s\s+/g', ' ') # replace multiple spaces with a single space
    text = text.replace(":)","happy")
    text = text.replace(":(","sad")
    text = re.sub ('\s+', ' ', text)
    text = re.sub('@[^\s]+','',text)  # delete the username
    text = re.sub('&[^\s]+','',text)
    text = re.sub('#[^\s]+','',text)
    text = re.sub('".*?"', '', text)  # delete anything in quotation marks
    text = re.sub('http[s]?://\S+', '', text) # delete urls
    for k, v in replace_words_dic.items():
        if k in text:
            text = re.sub(k,v,text)    
    text = text.replace("comfort delgro","comfortdelgro")       
    text = text.replace("as well as","and")
    text = text.replace("as well","also")
    text = text.replace("would like","shall")
    text = text.replace("should have","slightly negative")
    text = text.replace("could have","slightly negative")
    text = text.replace("would have","slightly negative")
    text = text.replace("would be","slightly negative")
    text = text.replace("could be","slightly negative")
    text = text.replace("should be","slightly negative")

    text = text.replace("n't","not")
    text = text.replace("n't","not")
    text = text.replace("don","not")
    text = text.replace("dun","not")
    text = text.replace("'s","is")
    text = text.replace("'s","is")
    text = text.replace("'ve","have")
    text = text.replace("'ve","have")
    text = text.replace("'d","had")
    text = text.replace("'d","had")
    text = text.replace("'ll","will")
    text = text.replace("'ll","will")
    text = text.replace("'re","are")
    text = text.replace("'re","are")
    text = text.replace("'m","am")
    text = text.replace("'m","am")
      
    text = text.replace("should improve","slightly negative")
    text = text.replace("would improve","slightly negative")
    text = text.replace("could improve","slightly negative")
    text = text.replace("would enhance","slightly negative")
    text = text.replace("could enhance","slightly negative")
    text = text.replace("would enhance","slightly negative")
    text = text.replace("to be honest","I will say")
    text = text.replace("it's like","alike")
    text = text.replace("middle finger","slightly negative")
    text = text.replace("snapped","slightly negative")
    text = text.replace("constantly accelerate","slightly negative") 
    text = text.replace("accelerate constantly","slightly negative")
    text = text.replace("accelerate and decelerate constantly","slightly negative") 
    text = text.replace("stopage","negative")
    text = text.replace("constantly accelerate and decelerate","slightly negative") 
    text = text.replace("extension service","good")
    text = text.replace("take advantage","slightly negative")
    text = text.replace("took advantage","slightly negative")
    text = text.replace("taking advantage","slightly negative")
    text = text.replace("takes advantage","slightly negative")
    #text = text.replace("please help","slightly negative")
    #text = text.replace("please","do") 
    
    text = re.sub("\S*@\S*\s?",'',text)   # delete email address
    text = text.replace('\n', ' ').replace('\r', '')  # Clean up all "\n"
    
    text = re.sub(r"""
               [)(@#&$]+  # Accept one or more copies of punctuation
               \ *           # plus zero or more copies of a space,
               """,
               "",          # and replace it with no space
               text, flags=re.VERBOSE)
    
    text = text.replace('.', ' .') #specially added to maintain fullstop
    text = text.replace('?', ' ?') #specially added to maintain question mark
    text = text.replace('!', ' !') #specially added to maintain exclamation mark
    text = text.replace(',', ' ,') #specially added to maintain exclamation mark
    text = text.replace(';', ' ;') #specially added to maintain exclamation mark
    text = text.replace(':', ' :') #specially added to maintain exclamation mark
    
    text= re.sub(' +', ' ', text)
    #text= re.sub(':', '', text)
    text= re.sub("[:']", '', text)
    #text = re.sub ('\s+', '', text)
    return text.lower()

##----------------------------------------------- Step 1 prof wang's standard english-----------------------------------------------##
def findPolarity(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 1 Prof Wang's standard english stage]
    1 if word found in prof wang standard el dict and if positive
    -1 if word found in prof wang standard el dict and if negative
    0 if word not found in prof or if it's not pos or neg

    Args:
        text (str): review

    Returns:
        list: polarity list
    """
    countList = []
    polaritylist = list(profwang_standard_el['Word'])
    for item in text.split(" "):
        #check if word has a polarity
        if item in polaritylist:
            senti = profwang_standard_el.loc[profwang_standard_el["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)  #coz prof wang standard el also contains negate words

        else: # word is a non polarity, negation or domain word
            countList.append(0)

    return countList


def countPolarity(scores):  # determine if review has a polarity, if so, find out the score from it.
    """ Counting overall polarity of the sentence.
    [Step 1 Prof Wang's standard english stage]

    Args:
        scores (list): polarity list

    Returns:
        int: overall sentiment number
    """
    if (1  in scores or -1 in scores):  #means have polarity  NEED TO CHANGE TO CHECK IF ALL O or not

        #Ambivalence handler  compare no. of 1s and -1s in score
        negativeoverall = scores.count(-1)
        positiveoverall = scores.count(1)

        if (positiveoverall > 0) and (negativeoverall ==0):
            return 1
        elif (negativeoverall > 0) and (positiveoverall ==0):
            return -1
        elif positiveoverall > negativeoverall:
            return 1
        elif negativeoverall > positiveoverall:
            return -1
        elif negativeoverall == positiveoverall:
            return -1
    return 0



##------------------------------------------- + step 2 prof wang's singlish english------------------------------------------------##
def findPolarity1(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 2 Prof Wang's standard english + Prof Wang's Singlish stage]

    1 if word found in prof wang standard el or singlish dict and if positive
    -1 if word found in prof wang standard el or singlish dict and if negative
    0 if word not found in prof or if it's not pos or neg

    Args:
        text (str): review

    Returns:
        list: polarity list
    """
    countList = []
    polaritylist = list(profwang_standard_el['Word'])
    singlishdict = list(profwang_singlish['Word'])
    for item in text.split(" "):
        #check if word has a polarity
        if item in polaritylist:
            senti = profwang_standard_el.loc[profwang_standard_el["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)

        elif item in singlishdict:
            senti = profwang_singlish.loc[profwang_singlish["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)

        else: # word is a non polarity, negation or domain word
            countList.append(0)


    return countList


def countPolarity1(scores):  # determine if review has a polarity, if so, find out the score from it.
    """ Counting overall polarity of the sentence.
    [Step 2 Prof Wang's standard english + Prof Wang's Singlish stage]

    Args:
        scores (list): polarity list

    Returns:
        int: overall sentiment number

    """
    if (1  in scores or -1 in scores):  #means have polarity  NEED TO CHANGE TO CHECK IF ALL O or not

        negativeoverall = scores.count(-1)
        positiveoverall = scores.count(1)

        if (positiveoverall > 0) and (negativeoverall ==0):
            return 1
        elif (negativeoverall > 0) and (positiveoverall ==0):
            return -1
        elif positiveoverall > negativeoverall:
            return 1
        elif negativeoverall > positiveoverall:
            return -1
        elif negativeoverall == positiveoverall:
            return -1
    return 0

#----------------------------------------------- + step 3 our english and singlish -----------------------------------------------##
def findPolarity2(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 3 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words]

    1 if word found in the dictionaries and if positive
    -1 if word found in the dictionaries and if negative
    0 if word not found in in the dictionaries or if it's not pos or neg

    Args:
        text (str): review

    Returns:
        list: polarity list
    """
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    for item in text.split(" "):
        #check if word has a polarity
        if item in polaritylist:
            senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)

        elif item in singlishdict:
            senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)

        else: # word is a non polarity, negation or domain word
            countList.append(0)


    return countList


def countPolarity2(scores):  # determine if review has a polarity, if so, find out the score from it.
    """ Counting overall polarity of the sentence.
    [Step 3 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words]

    Args:
        scores (list): polarity list

    Returns:
        int: overall sentiment number

    """
    if (1  in scores or -1 in scores):  #means have polarity  NEED TO CHANGE TO CHECK IF ALL O or not

        negativeoverall = scores.count(-1)
        positiveoverall = scores.count(1)

        if (positiveoverall > 0) and (negativeoverall ==0):
            return 1
        elif (negativeoverall > 0) and (positiveoverall ==0):
            return -1
        elif positiveoverall > negativeoverall:
            return 1
        elif negativeoverall > positiveoverall:
            return -1
        elif negativeoverall == positiveoverall:
            return -1

    return 0


## ----------------------------------------------------------------- + step 4 transport domain ----------------------------------------##
def findPolarity3(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 4 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words]

    1 if word found in the dictionaries and if positive
    -1 if word found in the dictionaries and if negative
    0 if word not found in in the dictionaries or if it's not pos or neg

    Args:
        text (str): review

    Returns:
        list: polarity list
    """
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    domainlist = list(domaindict["Word"])

    for item in text.split(" "):
        #check if word has a polarity
        if item in domainlist:
            countList.append(domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0])

        elif item in polaritylist:
            senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)

        elif item in singlishdict:
            senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
            if senti == "Negative":
                countList.append(-1)
            elif senti == "Positive":
                countList.append(1)
            else:
                countList.append(0)


        else: # word is a non polarity, negation or domain word
            countList.append(0)


    return countList


def countPolarity3(scores):  # determine if review has a polarity, if so, find out the score from it.
    """ Counting overall polarity of the sentence.
    [Step 4 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words]

    Args:
        scores (list): polarity list

    Returns:
        int: overall sentiment number

    """
    if (1  in scores or -1 in scores):  #means have polarity  NEED TO CHANGE TO CHECK IF ALL O or not

        #Ambivalence handler  compare no. of 1s and -1s in score
        negativeoverall = scores.count(-1)
        positiveoverall = scores.count(1)

        if (positiveoverall > 0) and (negativeoverall ==0):
            return 1
        elif (negativeoverall > 0) and (positiveoverall ==0):
            return -1
        elif positiveoverall > negativeoverall:
            return 1
        elif negativeoverall > positiveoverall:
            return -1
        elif negativeoverall == positiveoverall:
            return -1
    return 0


## -----------------------------------=----------------------------step 5 + negation ---------------------------------------------##
def findPolarity4(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 5 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation]

    1 if word found in the dictionaries and if positive
    -1 if word found in the dictionaries and if negative
    0 if word not found in in the dictionaries or if it's not pos or neg
    11 if word in the negation list
    (1, -7) if word is positive and will become neutral with negation
    (-1, -7) if word is negative and will become neutral with negation

    Args:
        text (str): review

    Returns:
        list: polarity list

    """
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    domainlist = list(domaindict["Word"])
    negateNeutral = pd.read_csv('negateneutral.csv', header = None)
    negateNeutral = pdColumn_to_list_converter(negateNeutral)
    for item in text.split(" "):

        #check if word has a polarity
        if item in domainlist:
            if item in negateNeutral:
                countList.append((domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0], -7))
            else:
                countList.append(domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0])

        elif item in polaritylist:
            if item in negateNeutral:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))   #-7 to mark that it is also a negate neutral word
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)   #just in case some neutral word is caught here

        elif item in singlishdict:
            if item in negateNeutral:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)

        #check if word in NEGATION list
        elif item in negation_list:
            countList.append(11)

        elif item == '.' or '?' or '!':
            countList.append(12)

        else: # word is a non polarity, negation or domain word
            countList.append(0)


    return countList


def countPolarity4(scores, k):  # determine if review has a polarity, if so, find out the score from it.
    """ Counting overall polarity of the sentence.
    [Step 5 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation]

    Negation word in front of a word found in negate neutral database would
    result in a polarity of 0 for that word.

    Negation will reverse the polarity of ther words
    Args:
        scores (list): polarity list
        k : distance for negation (either 6, 7 or 8 for distance of 5, 6 or 7 respectively)

    Returns:
        int: overall sentiment number

    Example:
        countPolarity4([-1, 11, (1, -7), 0, 0])
        >>>  negative

        countPolarity4([0, 11, (-1, -7), 0, 0])
        >>> neutral
        
        countPolarity4([0, 11, 1, 0, 0])
        >>>  negative

        countPolarity4([0, 11, -1  0, 0])
        >>> positive
                
        countPolarity4([-1, 0, 11, 0, 0, 0])
        >>>  negative

        countPolarity4([1, 0 11, 0  0, 0])
        >>> positive

        countPolarity4([0, 0, 11, 0, 0, 0, 0, 0, 1, 0, 0])
        >>>  positive (because the negative item(11) is too far from positive item (1).  The distance >5)

        countPolarity4([0, 0, 11, 0, 0, 1, 0, 0, 0, 0, 0])
        >>> negative (because the negative item(11) will act on positive item (1))
    """
    output_list = []
    #creating a new list #appending the relevant values afterwards
    scores_copy = scores.copy()
    for i in range(len(scores_copy)):

        if scores_copy[i] == 11:
            if i < (len(scores_copy)-1):
                negationIndex = i
                loop = True
                while loop == True:
                    for distance in range(1, k): #adjust number if needed
                        if i < (len(scores_copy)-distance) and len(scores_copy) > distance:
                            next_num = scores_copy[negationIndex + distance]
                            if type(next_num) != int:  #check for tuple  #checking for negate to neutral
                                output_list.append(0)
                                loop = False
                            elif next_num == 0:
                                output_list.append(11)
                                output_list.append(0)
                            elif next_num == 1:
                                output_list.append(-1)
                                loop = False
                            elif next_num == -1:
                                output_list.append(1)
                                loop = False
                            elif next_num == 12:
                                output_list.append(11)
                                output_list.append(12)
                                loop = False
                            else:
                                output_list.append(11)
                                output_list.append(next_num)
            else:
                output_list.append(11)  #if negation happens to be the last word strangely

        elif i == 0 or (i > 0 and scores_copy[i-1] != 11):
            if scores_copy[i] == 1 or scores_copy[i] == -1 or scores_copy[i] == 0:
                output_list.append(scores_copy[i])

            elif type(scores_copy[i]) != int:
                output_list.append(scores_copy[i][0])

            else:
                output_list.append(scores_copy[i])


    negativeoverall = output_list.count(-1)
    positiveoverall = output_list.count(1)

    if (negativeoverall== 0) and (positiveoverall==0):
        return 0
    else:
        if (positiveoverall > negativeoverall):
            return 1
        elif (negativeoverall > positiveoverall):
            return -1
        elif positiveoverall==negativeoverall:
            return -1


## ------------------------------------------------------------ step 6 + `too` handling -------------------------------------------##
## https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk

def findPolarity4_too(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 6 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation
    + 'Too' Handling]

   If 'too' is found in front of a word which is adjective, 'too' is mapped
   to -1 (negative) in polarity list, or else 0 by default.

    Args:
        text (str): review

    Returns:
        list: polarity list

    """
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    domainlist = list(domaindict["Word"])
    negateNeutral = pd.read_csv('negateneutral.csv', header = None)
    negateNeutral = pdColumn_to_list_converter(negateNeutral)
    for item in text.split(" "):
        if item == "too":
            word_list = word_tokenize(text)
            too_index = word_list.index(item)
            if too_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if pos_tagged_list[too_index+1][1] == "JJ":  #check if next word is adjective
                    countList.append(-1)
                else:
                    countList.append(0)

        #check if word has a polarity
        elif item in domainlist:
            if item in negateNeutral:
                countList.append((domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0], -7))
            else:
                countList.append(domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0])

        elif item in polaritylist:
            if item in negateNeutral:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))   #-7 to mark that it is also a negate neutral word
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)   #just in case some neutral word is caught here

        elif item in singlishdict:
            if item in negateNeutral:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)       #just in case some neutral word is caught here

        #check if word in NEGATION list
        elif item in negation_list:
            countList.append(11)

        elif item == '.' or '?' or '!':
            countList.append(12)

        else: # word is a non polarity, negation or domain word
            countList.append(0)


    return countList




## ------------------------------------------------------------ step 6.1 + `like` handling -------------------------------------------##
def findPolarity4_too_like(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 6 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation
    + 'Too' Handling + 'Like' Handling]

   If 'like' is found in behind of a word which is verb, 'like' is mapped
   to 0 (neutral) in polarity list.

    Args:
        text (str): review

    Returns:
        list: polarity list

    """
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    domainlist = list(domaindict["Word"])
    negateNeutral = pd.read_csv('negateneutral.csv', header = None)
    negateNeutral = pdColumn_to_list_converter(negateNeutral)
    for item in text.split(" "):
        if item == "too":
            word_list = word_tokenize(text)
            too_index = word_list.index(item)
            if too_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if pos_tagged_list[too_index+1][1] == "JJ":  #check if next word is adjective
                    countList.append(-1)
                else:
                    countList.append(0)

        if item == "like":
            word_list = word_tokenize(text)
            like_index = word_list.index(item)
            if like_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if (pos_tagged_list[like_index-1][1] == "VB") or (pos_tagged_list[like_index-1][1] =="VBD") or (pos_tagged_list[like_index-1][1] =="VBG") or (pos_tagged_list[like_index-1][1] =="VBN") or (pos_tagged_list[like_index-1][1] =="VBP") or (pos_tagged_list[like_index-1][1] =="VBZ"):  #check if next word is verb
                    countList.append(0)
                else:
                    countList.append(1)


        #check if word has a polarity
        elif item in domainlist:
            if item in negateNeutral:
                countList.append((domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0], -7))
            else:
                countList.append(domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0])

        elif item in polaritylist:
            if item in negateNeutral:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))   #-7 to mark that it is also a negate neutral word
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)   #just in case some neutral word is caught here

        elif item in singlishdict:
            if item in negateNeutral:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)       #just in case some neutral word is caught here

        #check if word in NEGATION list
        elif item in negation_list:
            countList.append(11)

        elif item == '.' or '?' or '!':
            countList.append(12)

        else: # word is a non polarity, negation or domain word
            countList.append(0)


    return countList


## ------------------------------------------------------------- step 7 + sarcasm ------------------------------------------------##
def is_subsequence(A, B):
    it = iter(A)
    return all(x in it for x in B)

def recognise_sarcasm(input_list):
    """ Detecting if the sentence has sarcasm
    [Step 7 Sarcasm]
    Returns -1 if sarcasm is detected and returns 0 if no sarcasm

    Args:
        scores (list): polarity list

    Returns:
        int: 0 or -1
    """
    if is_subsequence(input_list, [1, -1, 11]) or is_subsequence(input_list, [-1, 1, -1]) or is_subsequence(input_list, [-1, 11, 1]) or is_subsequence(input_list, [11, 1, 11]) or is_subsequence(input_list, [11, 1, -1]):
        return -1
    elif is_subsequence(input_list, [1, -1]) or is_subsequence(input_list, [11, 1]) or is_subsequence(input_list, [-1, 1]):
        return -1
    else:
        return 0

## remove or is_subsequence(input_list, [1, -1, 1])  or is_subsequence(input_list, [1, 11, 1]) or is_subsequence(input_list, [1, 11])
## added--or is_subsequence(input_list, [11, 1])
def flip(sarcasm,polarity_count):
    if sarcasm==-1:
        if polarity_count>0:
            return polarity_count*(-1)
        else:
            return polarity_count
    elif sarcasm==0:
        return polarity_count

## ---------------------------------------------------- step 8 + adversative ------------------------------------------------------##
def findPolarity5(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 8 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation
    + Too + Adversative]

    8 to represent 'after' type adversative. (eg. 'but')
    -8 to represent 'before' type adversative. (eg. 'even though')

    Args:
        text (str): review

    Returns:
        list: polarity list

    """
    text = text.strip()
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    domainlist = list(domaindict["Word"])
    negateNeutral = pd.read_csv('negateneutral.csv', header = None)
    negateNeutral = pdColumn_to_list_converter(negateNeutral)
    for item in text.split(" "):
        if item == "too":
            word_list = word_tokenize(text)
            too_index = word_list.index(item)
            if too_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if pos_tagged_list[too_index+1][1] == "JJ":  #check if next word is adjective
                    countList.append(-1)
                else:
                    countList.append(0)

        if item == "like":
            word_list = word_tokenize(text)
            like_index = word_list.index(item)
            if like_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if (pos_tagged_list[like_index-1][1] == "VB") or (pos_tagged_list[like_index-1][1] =="VBD") or (pos_tagged_list[like_index-1][1] =="VBG") or (pos_tagged_list[like_index-1][1] =="VBN") or (pos_tagged_list[like_index-1][1] =="VBP") or (pos_tagged_list[like_index-1][1] =="VBZ"):  #check if next word is verb
                    countList.append(0)
                else:
                    countList.append(1)

        #check if word has a polarity
        elif item in domainlist:
            if item in negateNeutral:
                countList.append((domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0], -7))
            else:
                countList.append(domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0])

        elif item in polaritylist:
            if item in negateNeutral:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)

        elif item in singlishdict:
            if item in negateNeutral:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)
                else:
                    countList.append(0)

        #check if word in NEGATION list
        elif item in negation_list:
            countList.append(11)

        elif item == '.' or '?' or '!':
            countList.append(12)

        else: # word is a non polarity, negation or domain word
            countList.append(0)

    for ad in before_adverse:
        if ad in text:
            startindex = text.index(ad)
            spaces = text[:startindex].count(" ")
            countList[spaces] = -8  # the word in before_adverse list
            for i in range(len(ad.split(" "))-1):
                del countList[spaces+1]

    for ad in after_adverse:
        if ad in text:
            startindex = text.index(ad)
            spaces = text[:startindex].count(" ")
            countList[spaces] = 8 # the word in after_adverse list
            for i in range(len(ad.split(" "))-1):
                del countList[spaces+1]

    return countList



def countPolarity5(input_list, k):
    """ Counting overall polarity of the sentence.
    [Step 8 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation
    + Too + Adversative]

    If 8 is present in the polarity list, only the polarities found after
    the adversative word is counted.

    If -8 is present in the polarity list, only the polarities found before
    the adversative word is counted.

    Args:
        scores (input_list): polarity list
        k : distance for negation (either 6, 7 or 8 for distance of 5, 6 or 7 respectively)

    Returns:
        int: overall sentiment number

    Example:
        countPolarity5([1, 11, (1, -7), -8, 0, -1])
        >>>  positive

        countPolarity5([1, 11, (-1, -7), 8, -1])
        >>> negative
    """

    negativescore=0
    positivescore=0
    neutralscore = 0

    adversative_present = False
    before  = False
    if -8 in input_list:   #before adverse has higher weightage than after adverse
        adverse_position = input_list.index(-8)
        before=True
        adversative_present = True
    elif 8 in input_list:
        adverse_position = input_list.index(8)
        before  = False
        adversative_present = True

    if adversative_present and before==True:
        new_adverse_list = input_list[:adverse_position]
        for i in range(len(new_adverse_list)):

            if new_adverse_list[i] == 11:
                if i < (len(new_adverse_list)-1):
                    negationIndex = i
                    loop = True
                    while loop == True:
                        for distance in range(1, k): #adjust number if needed
                            if i < (len(new_adverse_list)-distance) and len(new_adverse_list) > distance:
                                next_num = new_adverse_list[negationIndex + distance]
                                if type(next_num) != int:  #check for tuple  #checking for negate to neutral
                                    neutralscore += 1
                                    loop = False
                                elif next_num == 0:
                                    neutralscore += 1
                                elif next_num == 1:
                                    negativescore += 1
                                    loop = False
                                elif next_num == -1:
                                    positivescore += 1
                                    loop = False
                                elif next_num == 12:
                                    loop = False
                else:
                    neutralscore += 1  #if negation happens to be the last word strangely

            elif i == 0 or (i > 0 and new_adverse_list[i-1] != 11):
                if new_adverse_list[i] == 1:
                    positivescore += 1
                elif new_adverse_list[i] == -1:
                    negativescore += 1
                elif new_adverse_list[i] == 0:
                    neutralscore += 1
                elif type(new_adverse_list[i]) != int:
                    if new_adverse_list[i][0] == 1:
                        positivescore += 1
                    elif new_adverse_list[i][0] == 1:
                        negativescore += 1




    elif adversative_present and before == False:
        new_adverse_list = input_list[adverse_position + 1:]
        for i in range(len(new_adverse_list)):

            if new_adverse_list[i] == 11:
                if i < (len(new_adverse_list)-1):
                    negationIndex = i
                    loop = True
                    while loop == True:
                        for distance in range(1, k): #adjust number if needed
                            if i < (len(new_adverse_list)-distance) and len(new_adverse_list) > distance:
                                next_num = new_adverse_list[negationIndex + distance]
                                if type(next_num) != int:  #check for tuple  #checking for negate to neutral
                                    neutralscore += 1
                                    loop = False
                                elif next_num == 0:
                                    neutralscore += 1
                                elif next_num == 1:
                                    negativescore += 1
                                    loop = False
                                elif next_num == -1:
                                    positivescore += 1
                                    loop = False
                                elif next_num == 12:
                                    loop = False
                else:
                    neutralscore += 1  #if negation happens to be the last word strangely

            elif i == 0 or (i > 0 and new_adverse_list[i-1] != 11):
                if new_adverse_list[i] == 1:
                    positivescore += 1
                elif new_adverse_list[i] == -1:
                    negativescore += 1
                elif new_adverse_list[i] == 0:
                    neutralscore += 1
                elif type(new_adverse_list[i]) != int:
                    if new_adverse_list[i][0] == 1:
                        positivescore += 1
                    elif new_adverse_list[i][0] == 1:
                        negativescore += 1


    else: # no adversative words
        output_list = []
        #creating a new list #appending the relevant values afterwards
        for i in range(len(input_list)):

            if input_list[i] == 11:
                if i < (len(input_list)-1):
                    negationIndex = i
                    loop = True
                    while loop == True:
                        for distance in range(1, k): #adjust number if needed
                            if i < (len(input_list)-distance) and len(input_list) > distance:
                                next_num = input_list[negationIndex + distance]
                                if type(next_num) != int:  #check for tuple  #checking for negate to neutral
                                    output_list.append(0)
                                    loop = False
                                elif next_num == 0:
                                    output_list.append(11)
                                    output_list.append(0)
                                elif next_num == 1:
                                    output_list.append(-1)
                                    loop = False
                                elif next_num == -1:
                                    output_list.append(1)
                                    loop = False
                                elif next_num == 12:
                                    output_list.append(11)
                                    output_list.append(12)
                                    loop = False
                                else:
                                    output_list.append(11)
                                    output_list.append(next_num)
                else:
                    output_list.append(11)  #if negation happens to be the last word strangely

            elif i == 0 or (i > 0 and input_list[i-1] != 11):
                if input_list[i] == 1 or input_list[i] == -1 or input_list[i] == 0:
                    output_list.append(input_list[i])

                elif type(input_list[i]) != int:
                    output_list.append(input_list[i][0])

                else:
                    output_list.append(input_list[i])

        negativescore = output_list.count(-1)
        positivescore = output_list.count(1)



    if negativescore== 0 and positivescore==0:
        return 0
    else:
        if (positivescore > negativescore):
            return 1
        elif (negativescore > positivescore):
            return -1
        elif positivescore==negativescore and  adversative_present: # might have multiple layers of adversative
            return countPolarity5(new_adverse_list, k)
        elif positivescore==negativescore:
            return -1

## ---------------------------------- checking if adverative is present ---------------------------------------------##

def adversative_present(polarity_list):
    if (8 in polarity_list) or (-8 in polarity_list):
        return 1
    else:
        return 0

def update_p_after_adversative(present,polaritys, polaritya):
    if present==1:
        return polaritya
    elif present==0:
        return polaritys

def qn_mark(original_text, polarity):
    fivewoneh=['what','why','who','where','when','how', 'What','Why','Who','Where','When','How']
    if '?' in original_text:
        original_text = original_text.strip()
        if original_text.split(" ")[0] not in fivewoneh:
            polarity=-1
    else:
        polarity=polarity
    return polarity

##--------------------------------------------------step 9 + find emoji ---------------------------------------------##
def find_emoji(x):
    """ Finding polarity of the emoji if emoji is present.
    [Step 9 Emoji]

    0 - neutral emoji
    1 - positive emoji
    -1 - negative emoji

    Args:
        x (str): review

    Returns:
        int: 0 or -1 or 1

    """
    emoji_score = 0
    gotemoji = False
    for item in x:
        if item in emoji_list:
            emoji_score += emoji_dict[item]
            gotemoji = True
    if gotemoji == False:
        return 0
    elif emoji_score >0:
        return 1
    elif emoji_score <0:
        return -1
    else:
        return 0



##-----------------------------------------------------step 10 + multi -----------------------------------------------------##

def findPolarity6(text):
    """ Maps polarity to words and returns a polarity list.
    [Step 10 Prof Wang's standard english + Prof Wang's Singlish stage +
    our own English & Singlish words + Transport domain words + Negation
    + Too + Adversative + Multi]

    A - 4
    B - 2
    D - 0.5

    Args:
        text (str): review

    Returns:
        list: polarity list

    """
    text = text.strip()
    countList = []
    polaritylist = list(combined_standard_el['Word'])
    singlishdict = list(combined_singlish['Word'])
    domainlist = list(domaindict["Word"])
    negateNeutral = pd.read_csv('negateneutral.csv', header = None)
    negateNeutral = pdColumn_to_list_converter(negateNeutral)
    for item in text.split(" "):
        if item == "too":
            word_list = word_tokenize(text)
            too_index = word_list.index(item)
            if too_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if pos_tagged_list[too_index+1][1] == "JJ":  #check if next word is adjective
                    countList.append(-1)
                else:
                    countList.append(2)  # cuz 'too' belongs to group B in multi

        if item == "like":
            word_list = word_tokenize(text)
            like_index = word_list.index(item)
            if like_index < (len(word_list) - 1):
                pos_tagged_list = nltk.pos_tag(word_list)
                if (pos_tagged_list[like_index-1][1] == "VB") or (pos_tagged_list[like_index-1][1] =="VBD") or (pos_tagged_list[like_index-1][1] =="VBG") or (pos_tagged_list[like_index-1][1] =="VBN") or (pos_tagged_list[like_index-1][1] =="VBP") or (pos_tagged_list[like_index-1][1] =="VBZ"):  #check if next word is verb
                    countList.append(0)
                else:
                    countList.append(1)

        elif item in domainlist:
            if item in negateNeutral:
                countList.append((domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0], -7))
            else:
                countList.append(domaindict.loc[domaindict["Word"] == item, 'Sentiment Num'].values[0])

        elif item in polaritylist:
            if item in negateNeutral:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_standard_el.loc[combined_standard_el["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)

        elif item in singlishdict:
            if item in negateNeutral:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append((-1, -7))
                elif senti == "Positive":
                    countList.append((1, -7))
            else:
                senti = combined_singlish.loc[combined_singlish["Word"] == item, 'Sentiment'].values[0]
                if senti == "Negative":
                    countList.append(-1)
                elif senti == "Positive":
                    countList.append(1)

        #check if word in NEGATION list
        elif item in negation_list:
            countList.append(11)
                    #check if word in NEGATES TO NEUTRAL

        else: # word is a non polarity, negation or domain word
            countList.append(0)

    for ad in before_adverse:
        if ad in text:
            startindex = text.index(ad)
            spaces = text[:startindex].count(" ")
            countList[spaces] = -8  # the word in before_adverse list
            for i in range(len(ad.split(" "))-1):
                del countList[spaces+1]

    for ad in after_adverse:
        if ad in text:
            startindex = text.index(ad)
            spaces = text[:startindex].count(" ")
            countList[spaces] = 8 # the word in after_adverse list
            for i in range(len(ad.split(" "))-1):
                del countList[spaces+1]

    return countList



# ## -------------------------- Standalone Multi Function ---------------------------------- ##

def multi_value(polarity_list, text, final_polarity, k):
    """
    k means distance

    """
    text = text.strip()
    amp_dim_countlist = []
    amp_dim_values_mapping = {4: 1, 2: 0.75, 0.5: 0.25, 0: 0.35}
    for item in text.split(" "):
        if item in A:
            amp_dim_countlist.append(4)
        elif item in B:
            amp_dim_countlist.append(2)
        elif item in D:
            amp_dim_countlist.append(0.5)
        else:
            amp_dim_countlist.append(0)

    whether_equal_final_polarity = []
    for score in polarity_list:
        if score == final_polarity:
            whether_equal_final_polarity.append(1)
        else:
            whether_equal_final_polarity.append(0)


    for i in range(len(whether_equal_final_polarity)):
        if amp_dim_countlist[i] != 0:
            for distance in range(k):
                if distance <= len(amp_dim_countlist) - i:
                    return amp_dim_values_mapping[amp_dim_countlist[i]] * final_polarity

    return amp_dim_values_mapping[0] * final_polarity

def new_multi(value):
    if 0<value<=0.5:
        valuenew=1
    elif value==0:
        valuenew=0
    elif 1>=value>0.5:
        valuenew=2
    elif -0.5<=value<0:
        valuenew=-1
    elif -1<=value<-0.5:
        valuenew=-2
    return valuenew