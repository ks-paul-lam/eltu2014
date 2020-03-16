def main():
    import glob
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    import pickle

    # Parameters for Random Forest Classification
    parameters = {
        'max_features': 15000,    # Maximum Number of Distinct Word
        'criterion': 'entropy',  # Split Criterion
        'min_df': 50,             # Minimum Number of Occurrence of Feature
        'max_df': 0.80,           # Percentage of Used Features
        'n_estimators': 800,    # Number of Trees in the Forest
        'random_state': 17,      # Seed of Random
        'test_size': 0.8,        # Percentage of Test Data
        'min_n': 1,              # Minimum Number of N Gram
        'max_n': 1,              # Maximum Number of N Gram
    }

    for key, value in parameters.items():
        print(key, ' = ', value)

    # Initialization of
    nltk.download('stopwords')
    nltk.download('wordnet')
    wordnetlemmatizer = WordNetLemmatizer()
    listofstopwordenglish = stopwords.words('english')
    countvectorizer = CountVectorizer(max_features=parameters['max_features'],
                                      min_df=parameters['min_df'],
                                      max_df=parameters['max_df'],
                                      ngram_range=(parameters['min_n'], parameters['max_n']))
    tfidftransformer = TfidfTransformer()
    randomforestclassifier = RandomForestClassifier(n_estimators=parameters['n_estimators'],
                                                    random_state=parameters['random_state'])

    def text_preprocessor(line):
        line = re.sub(r'<br\s*/><br\s*/>', ' ', str(line))
        line = re.sub(r'[^a-zA-Z\-]', ' ', str(line))
        line = re.sub(r'(^|\s).(\s|$)', ' ', str(line))
        line = re.sub(r'\s{2,}', ' ', str(line))
        words = line.split()
        for i in range(len(words)):
            words[i] = words[i].lower()
            words[i] = wordnetlemmatizer.lemmatize(words[i], pos='v')
        words = [word for word in words if word not in listofstopwordenglish]
        return words

    def load_files_to_list(fileslist):
        x = []
        for filename in fileslist:
            try:
                with open(filename, encoding='utf-8') as f:
                    for line in f:
                        joint_text = ' '.join(text_preprocessor(line.strip()))
                    x.append(joint_text)
                pass
            except IOError as ioerror:
                if ioerror.errno != ioerror.EISDIR:
                    print(filename)
                    raise
        return x

    path = 'sentimental\\'
    path = path + '\\**\\*.txt'
    fileslist = glob.glob(path, recursive=True)
    fileslist_size = int(len(fileslist))
    fileslist_size_half = int(len(fileslist) / 2)

    x_prepro = load_files_to_list(fileslist)
    x_loaded_c = countvectorizer.fit_transform(x_prepro).toarray()
    x_loaded = tfidftransformer.fit_transform(x_loaded_c).toarray()

    y_loaded = [0 if i < fileslist_size_half else 1 for i in range(fileslist_size)]

    x_train, x_test, y_train, y_test = train_test_split(x_loaded,
                                                        y_loaded,
                                                        test_size=parameters['test_size'],
                                                        random_state=parameters['random_state'])

    sentimental = randomforestclassifier.fit(x_train, y_train)
    y_pred = randomforestclassifier.predict(x_test)

    with open('sentimental_countvectorizer.pickle', 'wb') as fin:
        pickle.dump(countvectorizer, fin)

    with open('sentimental_tfidftransformer.pickle', 'wb') as fin:
        pickle.dump(tfidftransformer, fin)

    with open('sentimental_mlmodel.pickle', 'wb') as fin:
        pickle.dump(sentimental, fin)

    feature_names_list = [k for k in countvectorizer.vocabulary_]
    print(len(feature_names_list))

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))


if __name__ == '__main__':
    main()
