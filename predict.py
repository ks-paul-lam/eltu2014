def main(s, *args, **kwargs):
    from random import seed
    from random import randint
    from nltk.stem import WordNetLemmatizer
    import pickle
    import re
    from os import system, name

    def clear():
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

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

    def print_menu(title, year, number_of_pos, number_of_neg, number_of_truth, number_of_fake, number_of_s):
        print('Title: ', title, '\nYear: ', year, '\n----------------')
        print('1. Random Pos. Review (%2.2f %%)' % (number_of_pos / number_of_truth * 100))
        print('2. Random Neg. Review (%2.2f %%)' % (number_of_neg / number_of_truth * 100))
        print('3. Random Dec. Review (%2.2f %%)' % (number_of_fake / number_of_s * 100))
        print('4. Back')

    if (s == []):
        s = [input("Input your review: ")]
    else:
        title = kwargs.get('title', None)
        year = kwargs.get('year', None)

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

    number_of_s = len(s)

    if (number_of_s == 1):
        print(s[0])

        pred = deceptive_test_string(format_string(s[0]))

        if (pred == 'deceptive'):
            print("This is a deceptive review.\n")
        elif (pred == 'truth'):
            sentimental_pred = sentimental_test_string(format_string(s[0]))
            if (sentimental_pred):
                print("This is a positive review.\n")
            else:
                print("This is a negative review.\n")
    else:
        processed = 0
        pred_truth = []
        pred_fake = []
        for line in s:
            if(deceptive_test_string(format_string(line)) == 'truth'):
                pred_truth.append(line)
            elif (deceptive_test_string(format_string(line)) == 'deceptive'):
                pred_fake.append(line)
            processed += 1
            print(processed, ' reviews processed.', end='\r')

        number_of_truth = len(pred_truth)
        number_of_fake = len(pred_fake)

        result_pos = []
        result_neg = []

        processed = 0
        for line in pred_truth:
            sentimental_pred = sentimental_test_string(format_string(line))
            if (sentimental_pred):
                result_pos.append(line)
                # print("This is a positive review.\n")
            else:
                result_neg.append(line)
                # print("This is a negative review.\n")
            processed += 1
            print(processed, ' reviews classified.', end='\r')

        number_of_pos = len(result_pos)
        number_of_neg = len(result_neg)

        seed(1)
        clear()
        while(1):
            print_menu(title, year, number_of_pos, number_of_neg, number_of_truth, number_of_fake, number_of_s)
            try:
                choice = int(input('Your choice: '))
            except ValueError:
                choice = -1

            if (choice == 1):
                random_int = randint(0, number_of_pos)
                clear()
                print('----------------')
                print(result_pos[random_int])
                print('----------------')
                pass
            elif(choice == 2):
                random_int = randint(0, number_of_neg)
                clear()
                print('----------------')
                print(result_neg[random_int])
                print('----------------')
                pass
            elif(choice == 3):
                random_int = randint(0, number_of_fake)
                clear()
                print('----------------')
                print(pred_fake[random_int])
                print('----------------')
                pass
            elif(choice == 4):
                break
            else:
                print("Invalid Input.\n")


if __name__ == '__main__':
    main()
