from flask import Flask, render_template, request
import nltk
import Api as Api
import Processes as Process


# nltk.download()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        moviename = request.form.get('Mname') # Get the movie name from the form
        drescribingwords = request.form.get('Dname') # Get the movie name from the form
        drescribingwords = int(drescribingwords)
        id = Api.Getid(moviename) # Get the movie ID from the API
        if not id:
            return render_template("error.html")
        
        detailsofsearch = Api.GetDetails(id)
        if not detailsofsearch:
            return render_template("error.html")
        
        image = Api.GetImage(id)
        if not image:
            return render_template("error.html")
        
        imageoutput = Api.GetPoster(image)
        if not imageoutput:
            return render_template("error.html")
        
        keywords = Api.GetKeywords(id)
        if not keywords:
            return render_template("error.html")
        
        keyword_text = ', '.join(keywords)
        
        trailer = Api.GetTrailer(id)
        if not trailer:
            return render_template("error.html")

        all = []
        for comment in detailsofsearch: # Loop through the comments
            print(comment)
            processed = Process.processor(comment) 
            lemmatized_text = ' '.join(processed)
            print(lemmatized_text)
            top_words = Process.tfidf(lemmatized_text)
            print(top_words)
            top_words_string = ', '.join(top_words)
            all.append(top_words_string)
            print(top_words_string)
            holder = Process.sentiment(top_words_string)
            print(holder)
            
        topwordsglobal = all
        print(topwordsglobal)
        topwordsglobal = ' '.join(topwordsglobal)
        globalwords = Process.globaltopwords(topwordsglobal,drescribingwords)
        globalwords = ', '.join(globalwords)
        print(globalwords)
        
        avg = Process.getscore(holder)
        print(avg)
        sentimentoutput = Process.sentimentoutput(avg)
        icon = sentimentoutput[0]
        sentiment = sentimentoutput[1]
        print(icon)
        return render_template(
            "results.html",
            words=keyword_text,
            imageoutput=imageoutput,
            compoundscore=avg,
            moviename=moviename,
            icon=icon,
            sentiment=sentiment,
            trailer=trailer,
            globalwords = globalwords
        )

    # Render the index.html template for GET requests
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
