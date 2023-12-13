import json

from flask import Flask, redirect, session, url_for, render_template, request, abort
from authlib.integrations.flask_client import OAuth

from projectsecrets import secret_key, spotify_client_id, spotify_client_secret

app = Flask(__name__)
app.secret_key = secret_key

oauth = OAuth(app)
oauth.register(
    name="spotify",
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    authorize_url="https://accounts.spotify.com/authorize",
    access_token_url="https://accounts.spotify.com/api/token",
    api_base_url="https://api.spotify.com/v1/",
    client_kwargs={
        'scope': 'playlist-read-private user-top-read'
    }
)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        token = session["spotify-token"]
    except KeyError:
        return redirect(url_for("login"))
    print(dir(oauth.spotify))
    data = oauth.spotify.get("search?q=PostMalone&type=artist&limit=1", token=token).text
    artistData = json.loads(data)["artists"]["items"]
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'],)
def results():
    Artist1 = request.form.get('Artist1')
    Artist2 = request.form.get('Artist2')
    try:
        token = session["spotify-token"]
    except KeyError:
        return redirect(url_for("login"))
    print(dir(oauth.spotify))
    data = oauth.spotify.get("search?q="+Artist1+"&type=artist&limit=1", token=token).text
    artistData1 = json.loads(data)["artists"]["items"]
    data = oauth.spotify.get("search?q="+Artist2+"&type=artist&limit=1", token=token).text
    artistData2 = json.loads(data)["artists"]["items"]
    popularity1 = artistData1[0]["popularity"]
    popularity2 = artistData2[0]["popularity"]

    finalArtist1 = artistData1
    finalArtist2 = artistData2
    if popularity1 < popularity2:
        finalArtist1 = artistData2
        finalArtist2 = artistData1

    if popularity1 == popularity2:
        image1 = finalArtist1[0]["images"][0]["url"]
        image2 = finalArtist2[0]["images"][0]["url"]
        name1 = finalArtist1[0]["name"]
        name2 = finalArtist2[0]["name"]
        fol1 = finalArtist1[0]["followers"]["total"]
        fol2 = finalArtist2[0]["followers"]["total"]
        fol1 =  "{:,}".format(fol1)
        fol2 =  "{:,}".format(fol2)
        gen1 = (finalArtist1[0]["genres"])
        gen2 = (finalArtist2[0]["genres"])
        capitalized_genres1 = [genre.capitalize() for genre in gen1]
        gen1final = ", ".join(capitalized_genres1)
        capitalized_genres2 = [genre.capitalize() for genre in gen2]
        gen2final = ", ".join(capitalized_genres2)
        return render_template("equal.html", url1 = image1, url2 = image2, name1 = name1, name2= name2, fol1 = fol1, fol2 = fol2, gen1 = gen1final, gen2 = gen2final)
    else:
        image1 = finalArtist1[0]["images"][0]["url"]
        image2 = finalArtist2[0]["images"][0]["url"]
        name1 = finalArtist1[0]["name"]
        name2 = finalArtist2[0]["name"]
        fol1 = finalArtist1[0]["followers"]["total"]
        fol2 = finalArtist2[0]["followers"]["total"]
        fol1 =  "{:,}".format(fol1)
        fol2 =  "{:,}".format(fol2)
        gen1 = (finalArtist1[0]["genres"])
        gen2 = (finalArtist2[0]["genres"])
        capitalized_genres1 = [genre.capitalize() for genre in gen1]
        gen1final = ", ".join(capitalized_genres1)
        capitalized_genres2 = [genre.capitalize() for genre in gen2]
        gen2final = ", ".join(capitalized_genres2)
        return render_template("results.html", url1 = image1, url2 = image2, name1 = name1, name2= name2, fol1 = fol1, fol2 = fol2, gen1 = gen1final, gen2 = gen2final)


@app.route("/login")
def login():
    redirect_uri = url_for('authorize', _external=True)
    print(redirect_uri)
    return oauth.spotify.authorize_redirect(redirect_uri)


@app.route("/spotify-authorize")
def authorize():
    token = oauth.spotify.authorize_access_token()
    session["spotify-token"] = token
    return token

