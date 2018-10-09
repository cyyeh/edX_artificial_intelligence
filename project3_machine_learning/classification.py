import numpy as np
import sys
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

def main():
    if len(sys.argv) == 3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

        features = []
        labels = []

        with open(input_file_name, mode='r') as f:
            lines = f.read().splitlines()
            for line in lines[1:]:
                features.append([float(val) for val in line.split(',')[:-1]])
                labels.append(float(line.split(',')[-1]))

        x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.4, random_state=0, stratify=labels)
        
        with open(output_file_name, mode='w') as f:
            # SVM with Linear Kernel
            parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
            svc_linear = svm.SVC(kernel='linear')
            clf = GridSearchCV(svc_linear, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('svm_linear,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n')

            # SVM with Polynomial Kernel
            parameters = {'C': [0.1, 1, 3], 'degree': [4, 5, 6], 'gamma': [0.1, 0.5]}
            svc_poly = svm.SVC(kernel='poly')
            clf = GridSearchCV(svc_poly, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('svm_polynomial,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n') 

            # SVM with RBF Kernel
            parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}
            svc_rbf = svm.SVC(kernel='rbf')
            clf = GridSearchCV(svc_rbf, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('svm_rbf,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n')                      

            # Logistic Regression
            parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
            logistic_regression = LogisticRegression()
            clf = GridSearchCV(logistic_regression, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('logistic,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n')

            # k-Nearest Neighbors
            parameters = {'n_neighbors': list(range(1, 51)), 'leaf_size': [num for num in range(5, 61) if num % 5 == 0]}
            k_nearest_neighbors = KNeighborsClassifier()
            clf = GridSearchCV(k_nearest_neighbors, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('knn,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n')

            # decision trees
            parameters = {'max_depth': list(range(1, 51)), 'min_samples_split': list(range(2, 11))}
            decision_tree = DecisionTreeClassifier()
            clf = GridSearchCV(decision_tree, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('decision_tree,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n')   

            # random forests
            parameters = {'max_depth': list(range(1, 51)), 'min_samples_split': list(range(2, 11))}
            random_forests = RandomForestClassifier()
            clf = GridSearchCV(random_forests, parameters, cv=5)
            clf.fit(x_train, y_train)
            f.write('random_forest,' + str(clf.best_score_) + ',' + str(clf.score(x_test, y_test)) + '\n')             
    else:
        print('Usage:', sys.argv[0], "input_file, output_file")
        sys.exit(1)
            
    
if __name__ == "__main__":
    main()