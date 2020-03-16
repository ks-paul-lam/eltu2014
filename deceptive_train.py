def main():
    import os
    import fnmatch
    from textblob import TextBlob
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from nltk.corpus import stopwords
    import regex as re
    from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn import svm
    from sklearn.model_selection import GridSearchCV
    import pickle

    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    def pos(review_without_stopwords):
        return TextBlob(review_without_stopwords).tags

    def svc_param_selection(X, y, nfolds):
        Cs = [0.001, 0.01, 0.1, 1, 10]
        gammas = [0.001, 0.01, 0.1, 1]
        param_grid = {'C': Cs, 'gamma': gammas}
        grid_search = GridSearchCV(svm.SVC(kernel='linear'), param_grid, cv=nfolds)
        grid_search.fit(X, y)
        return grid_search.best_params_

    path = 'deception\\'

    label = []

    configfiles = [os.path.join(subdir, f)
                   for subdir, dirs, files in os.walk(path)
                   for f in fnmatch.filter(files, '*.txt')]

    for f in configfiles:
        c = re.search('(trut|deceptiv)\w', f)
        label.append(c.group())

    labels = pd.DataFrame(label, columns=['Labels'])

    review = []
    directory = os.path.join(path)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.filter(files, '*.txt'):
                f = open(os.path.join(subdir, file), 'r')
                a = f.read()
                review.append(a)

    reviews = pd.DataFrame(review, columns=['HotelReviews'])

    result = pd.merge(reviews, labels, right_index=True, left_index=True)
    result['HotelReviews'] = result['HotelReviews'].map(lambda x: x.lower())

    stop = stopwords.words('english')
    result['review_without_stopwords'] = result['HotelReviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    os = result.review_without_stopwords.apply(pos)
    os1 = pd.DataFrame(os)

    os1['pos'] = os1['review_without_stopwords'].map(lambda x: " ".join(["/".join(x) for x in x]))

    result = result = pd.merge(result, os1, right_index=True, left_index=True)

    review_train, review_test, label_train, label_test = train_test_split(result['pos'], result['Labels'], test_size=0.2, random_state=17)

    tf_vect = TfidfVectorizer(lowercase=True, use_idf=True, smooth_idf=True, sublinear_tf=False)
    X_train_tf = tf_vect.fit_transform(review_train)
    X_test_tf = tf_vect.transform(review_test)

    parameters = svc_param_selection(X_train_tf, label_train, 5)

    clf = svm.SVC(C=parameters['C'], gamma=parameters['gamma'], kernel='linear')
    clf.fit(X_train_tf, label_train)
    pred = clf.predict(X_test_tf)

    with open('deceptive_vectorizer.pickle', 'wb') as fin:
        pickle.dump(tf_vect, fin)

    with open('deceptive_mlmodel.pickle', 'wb') as f:
        pickle.dump(clf, f)

    X_test_tf = tf_vect.transform(review_test)
    pred = clf.predict(X_test_tf)

    print(accuracy_score(label_test, pred))
    print(confusion_matrix(label_test, pred))
    print(classification_report(label_test, pred))


if __name__ == '__main__':
    main()
