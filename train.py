from os import system
import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score

class Train:

    def __init__(self):
        self.model = tree.DecisionTreeClassifier(criterion='entropy')
        self.data = data
        self.header_list = header_list

    def build_tree(self, header_list, data):
        X = self.data.values[0:70, 0:6]
        y = self.data.values[0:70, 6:7]

        self.model.fit(X, y)
        self.model.score(X, y)
        print("Tree have already built")

    def get_tree_dot(self):
        tree.export_graphviz(self.model,
                             out_file='tree.dot',
                             filled=True)
        print("Got tree.dot")
    def get_tree_png(self):
        system("dot -Tpng tree.dot -o tree2.png")
    def get_model(self):
        print("Got model")
        return self.model


    def get_predicted_value(self,data_to_predict):
        predicted = self.model.predict(data_to_predict)
        print(predicted)
        return predicted

    # get_predicted_value(x_test)
header_list = ['waitings_client', 'orders_to_kitchen', 'dishes_waiting_for_delivery', 'actual_collecing1','actual_collecing2', 'actual_collecing3', 'result_state']
data = pd.read_csv('./src/newTrainingSet.csv', sep=',', header=None)

train = Train()
train.build_tree(header_list, data)
train.get_tree_dot()
train.get_model()
train.get_tree_png()
x_test = data.values[70:99, 0:6]
train.get_predicted_value(x_test)