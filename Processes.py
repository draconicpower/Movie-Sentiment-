import PreProcessing as Clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as Vader
from sklearn.feature_extraction.text import TfidfVectorizer

# pip install vaderSentiment


def processor(comment):
    tokenizer = Clean.whiteSpaceTokenization(comment)
    stopwordRemoved = Clean.removeStopWord(tokenizer)
    Cleaner = Clean.cleanText(stopwordRemoved)
    lemmatizedTokens = Clean.lemmatize(Cleaner)
    return lemmatizedTokens


def tfidf(text):
    # Create a TF-IDF vectorizer object
    vectorizer = TfidfVectorizer(stop_words='english')
    # Check if the text is empty or contains only non-alphabetic characters
    if not text.strip() or not text.replace(" ", "").isalpha():
        return []
    else:
        try:
            tfidf_matrix = vectorizer.fit_transform(
                [text])  # Fit the vectorizer to the text
        except ValueError:
            # Print an error message if the computation fails
            print("TF-IDF computation error, skipping comment.")
            return []
        # Convert the sparse matrix to a dense array
        tfidf_array = tfidf_matrix.toarray()[0]
        feature_names = vectorizer.get_feature_names_out()  # Get the feature names
        # Create a dictionary of feature names and their TF-IDF scores
        tfidf_dict = dict(zip(feature_names, tfidf_array))
        sorted_tfidf = sorted(tfidf_dict.items(),
                              # Sort the dictionary by TF-IDF score in descending order
                              key=lambda x: x[1], reverse=True)
        # Get the top 20 words
        top_words = [word for word, score in sorted_tfidf[:20]]
        return top_words


def globaltopwords(text,dw):
        # Create a TF-IDF vectorizer object
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([text]) # Fit the vectorizer to the text
        except ValueError:
            print("TF-IDF computation error, skipping comment.") 
            return []
        tfidf_array = tfidf_matrix.toarray()[0] # Convert the sparse matrix to a dense array
        feature_names = vectorizer.get_feature_names_out() # Get the feature names
        tfidf_dict = dict(zip(feature_names, tfidf_array)) # Create a dictionary of feature names and their TF-IDF scores
        sorted_tfidf = sorted(tfidf_dict.items(),
                              key=lambda x: x[1], reverse=True) # Sort the dictionary by TF-IDF score in descending order
        top_words = [word for word, score in sorted_tfidf[:dw]] # Get the top 20 words
        return top_words
    


def sentiment(text):
    holder = []
    # Calculate the sentiment score using Vader for the top words string
    sentiment_scores = Vader().polarity_scores(text)
    # Convert the sentiment score to a 0-100 scale
    compound_score = (sentiment_scores['compound'] + 1) * 50
    compound_score = round(compound_score, 2)
    # Append the sentiment score to the list of sentiment scores
    holder.append(compound_score)
    return holder


def getscore(holder):
    lenght = len(holder)
    totalscore = sum(holder)
    avg = totalscore / lenght
    return avg


def sentimentoutput(avg):
    
    if avg <= 10:
        sentiment = "Abysmal Sentiment"
        icon = 'fa-solid fa-face-dizzy'
    elif avg <= 20:
        sentiment = "Terrible Sentiment"
        icon = 'fa-solid fa-face-sad-tear'
    elif avg <= 40:
        sentiment = "Negative Sentiment"
        icon = 'fa-solid fa-face-frown'
    elif 40 < avg <= 50:
        sentiment = "Neutral Sentiment"
        icon = 'fa-solid fa-face-meh'
    elif avg <= 70:
        sentiment = "Positive Sentiment"
        icon = 'fa-solid fa-face-smile'
    elif avg <= 90:
        sentiment = "Amazing Sentiment"
        icon = 'fa-solid fa-face-grin-wide'
    else:
        sentiment = "Stellar Sentiment"
        icon = 'fa-solid fa-face-grin-stars'
        
    return icon, sentiment

