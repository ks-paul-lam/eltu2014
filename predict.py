def main():
    from nltk.stem import WordNetLemmatizer
    import pickle
    import re

    def text_preprocessor(line):
        wordnetlemmatizer = WordNetLemmatizer()
        line = re.sub(r'<br\s*/><br\s*/>', ' ', str(line))
        line = re.sub(r'[^a-zA-Z\-]', ' ', str(line))
        line = re.sub(r'(^|\s).(\s|$)', ' ', str(line))
        line = re.sub(r'\s{2,}', ' ', str(line))
        words = line.split()
        for i in range(len(words)):
            words[i] = words[i].lower()
            words[i] = wordnetlemmatizer.lemmatize(words[i], pos='v')
        return words

    def format_string(s):
        joint_text = ' '.join(text_preprocessor(s.strip()))
        return joint_text

    def deceptive_test_string(s):
        X_test_tf = deceptive_tf_vect.transform([s])
        y_predict = deceptive_clf.predict(X_test_tf)
        return y_predict

    def sentimental_test_string(s):
        X_loaded_c = sentimental_tf_cvect.transform([s]).toarray()
        X_test_tf = sentimental_tf_vect.fit_transform(X_loaded_c).toarray()
        y_predict = sentimental_clf.predict(X_test_tf)
        return y_predict

    s = input("Input your review: ")

    s = format_string(s)

    deceptive_vec = open('deceptive_vectorizer.pickle', 'rb')
    deceptive_tf_vect = pickle.load(deceptive_vec)

    deceptive_pkl = open('deceptive_mlmodel.pickle', 'rb')
    deceptive_clf = pickle.load(deceptive_pkl)

    sentimental_cvec = open('sentimental_countvectorizer.pickle', 'rb')
    sentimental_tf_cvect = pickle.load(sentimental_cvec)

    sentimental_vec = open('sentimental_tfidftransformer.pickle', 'rb')
    sentimental_tf_vect = pickle.load(sentimental_vec)

    sentimental_pkl = open('sentimental_mlmodel.pickle', 'rb')
    sentimental_clf = pickle.load(sentimental_pkl)

    pred = deceptive_test_string(s)

    if (pred == 'deceptive'):
        print("This is a deceptive review.\n")
    elif (pred == 'truth'):
        sentimental_pred = sentimental_test_string(s)
        if (sentimental_pred):
            print("This a positive review.\n")
        else:
            print("This a negative review.\n")


if __name__ == '__main__':
    main()
