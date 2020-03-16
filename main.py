import predict
import imdb
import deceptive_train
import sentimental_train


while (1):
    try:
        choice = int(input("1. Train\n2. Predict\n3. Search\n4. Exit\nYour choice: "))
    except ValueError:
        choice = -1

    if (choice == 1):
        deceptive_train.main()
        sentimental_train.main()
        pass
    elif(choice == 2):
        predict.main([])
        pass
    elif(choice == 3):
        imdb.main()
        pass
    elif(choice == 4):
        break
    else:
        print("Invalid Input.\n")
