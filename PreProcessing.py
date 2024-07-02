import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as lemmatizer
from nltk import word_tokenize, pos_tag, ne_chunk

#nltk.download()

#Transforms tokens into their root form using lemmatization

def whiteSpaceTokenization(input_data):
    tokens = []
    
    # Check if input_data is a list or a string
    if isinstance(input_data, list):
        # Iterate through each element in the list (assuming each element is a string)
        for text in input_data:
            # Tokenize the string by splitting on whitespace and extend the tokens list
            tokens.extend(text.split())
    elif isinstance(input_data, str):
        # If the input is a string, split it directly
        tokens = input_data.split()
    else:
        # If input_data is neither list nor string, raise an error
        raise ValueError("Input data must be a list of strings or a single string")
    
    return tokens

    
def lemmatize(tokenList) :
    #List of lemmatized words
    lemma = []
    #create a lemmatizer object
    lem = lemmatizer()
    #For every token in the inputted tokenList
    for token in tokenList:
        # Change the current token to its root form - use the lowercase version of the token due to capitals
        lemmatizedWord = lem.lemmatize(token.lower())
        # Add it to the list of lemmatized words
        lemma.append(lemmatizedWord)
    #return th elist of lemmatized words
    return lemma

def removeStopWord(tokenList):
    #list of words without stop words
    filtered_words = []
    #for every word in the input token list
    for word in tokenList:
        #Check if the word (in lower case) is a stopword, if not - add it to the list of filtered words
        if not word.lower() in stopwords.words('english'):
            filtered_words.append(word)
    #return the list of words without stopwords
    return  filtered_words

def cleanText(tokenList):
    # List of actual words
    wordList = []

    # Tagging each token with part-of-speech (POS) tags
    pos_tagged = pos_tag(tokenList)
    
    # Perform named entity recognition using NLTK's ne_chunk
    ne_tree = ne_chunk(pos_tagged)
    
    # Set to keep track of person entities
    persons = set()
    
    # Walk through the tree to find PERSON entities
    for subtree in ne_tree: # Iterate through the tree to find PERSON entities
        if hasattr(subtree, 'label'): # Check if the subtree has a label attribute
            if subtree.label() == 'PERSON': # Check if the label is PERSON
                # If the subtree is a PERSON entity, add each leaf (word) to the persons set
                person_name = ' '.join(leaf[0] for leaf in subtree.leaves()) # Join the leaves to form the person's name
                persons.add(person_name.lower()) # Add the person's name to the set of persons
    
    # Filter out names (persons) from the token list
    for token in tokenList:
        # Convert token to lowercase for case-insensitive comparison
        lowercased_token = token.lower()
        # Check whether the token is alphabetic and not in the persons set
        if token.isalpha() and lowercased_token not in persons:
            # If the token is not a person, add it to the wordList
            wordList.append(token)
    # Return the list of words without names
    return wordList


