import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():

    if request.method== 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            imdb_url = "https://www.imdb.com/search/title/?count=100&title_type=feature,tv_series&ref_=nv_wl_img_2" + searchString
            uClient = uReq(imdb_url)
            imdbPage = uClient.read()
            uClient.close()
            imdb_html = bs(imdbPage, "html.parser")

            content = imdb_html.find(id="main")
            movieframe= content.find_all("div", class_="lister-item mode-advanced")

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)

            reviews = []

            for movie in movieframe:

                # moviecontentbox = movie.find("div",class_="lister-item-content")
                movieFirstLine = movie.find("h3", class_="lister-item-header")
                movieTitle =(movieFirstLine.find("a").text)
                movieDate = (re.sub(r"[()]", "", movieFirstLine.find_all("span")[-1].text))
                try:
                    movieRunTime=(movie.find("span", class_="runtime").text[:-4])
                except:
                    movieRunTime ='No name'

                movieGenre=(movie.find("span", class_="genre").text.rstrip().replace("\n", "").split(","))

                try:
                    movieRating =(movie.find("strong").text)
                except:
                    movieRating = "No name"

                # try:
                #     movieScore =(movie.find("span", class_="metascore unfavorable").text.rstrip().replace("\n", "").split(","))
                # except:
                #     movieScore = "No name"

                movieDescription =(movie.find_all("p", class_="text-muted")[-1].text.lstrip())

                movieCast = movie.find("p", class_="")

                try:
                    casts = movieCast.text.replace("\n", "").split('|')
                    casts = [x.strip() for x in casts]
                    casts = [casts[i].replace(j, "") for i, j in enumerate(["Director:", "Stars:"])]
                    movieDirector=(casts[0])
                    movieStars=([x.strip() for x in casts[1].split(",")])
                except:
                    casts = movieCast.text.replace("\n", "").strip()
                    movieDirector = "No name"
                    movieStars =([x.strip() for x in casts.split(",")])

                # movieNumbers = movie.find_all("span", attrs={"name": "nv"})
                #
                # if len(movieNumbers) == 2:
                #     movieVotes=(movieNumbers[0].text)
                #     movieGross=(movieNumbers[1].text)
                # elif len(movieNumbers) == 1:
                #     movieVotes=(movieNumbers[0].text)
                #     movieGross= "No name"
                # else:
                #     movieVotes="No name"
                #     movieGross= "No name"

                movieData = {"Movies": movieTitle, "Name": movieDate,
                         "Rating": movieRunTime, "CommentHead": movieGenre,
                         "Comment": movieRating,"MoviesDescriptions": movieDescription,
                       "MoviesStars": movieStars}

                        #"MoviesScores": movieScore,
                        # "MoviesDescriptions": movieDescription,
                        # "MoviesDirectors": movieDirector, "MoviesStars": movieStars,
                        # "MoviesAllVotes": movieVotes, "MoviesGross": movieGross}

                reviews.append(movieData)

            return render_template('results.html',reviews=reviews[0:(len(reviews) - 1)])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=8001, debug=True)