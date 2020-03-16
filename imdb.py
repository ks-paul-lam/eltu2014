def main():

    import json
    import requests
    from bs4 import BeautifulSoup
    import predict

    title = input("Search by title: ")
    omdbapi_url = "http://www.omdbapi.com/?t=" + title + "&apikey=1fb69a60"
    s = requests.session()
    r = s.get(omdbapi_url)
    omdbapi_reponse = json.loads(r.text)

    reviews = []

    if (omdbapi_reponse['Response'] == 'True'):
        imdbID = omdbapi_reponse['imdbID']
        title = omdbapi_reponse['Title']
        year = omdbapi_reponse['Year']
    elif (omdbapi_reponse['Response'] == 'False'):
        print(omdbapi_reponse['Error'])
        return reviews

    imdb_url = "https://www.imdb.com/title/" + imdbID + "/reviews/_ajax?"

    while True:
        r = s.get(imdb_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for div in soup.findAll('div', 'text show-more__control'):
            reviews.append(div.text)

        load_more_data = soup.findAll('div', 'load-more-data')
        if load_more_data == []:
            break
        else:
            imdb_url = 'http://www.imdb.com/title/' + imdbID + '/reviews/_ajax?paginationKey=' + load_more_data[0]['data-key']

    predict.main(reviews, title=title, year=year)


if __name__ == '__main__':
    main()
