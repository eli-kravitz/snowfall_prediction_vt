import numpy as npclass NeuralNetwork():        def __init__(self, input_size, output_size, hidden_size, n, lr, lrb):                '''        Description:            Initialize feed forward NN class                Inputs:            input_size: int                number of inputs            output_size: int                number of outputs            hidden_size: int                number of nodes in single hidden layer            n: int                number of training samples            lr: float                learning rate for weights            lrb: float                learning rate for biases                    Outputs:            N/A        '''                self.input_size = input_size        self.output_size = output_size        self.hidden_size = hidden_size        self.n = n        self.lr = lr        self.lrb = lrb                # Random initialization of weights from input layer to hidden layer        self.W1 = np.random.randn(self.input_size, self.hidden_size) # c by h                 # Random initialization of weights from hidden layer to output layer        self.W2 = np.random.randn(self.hidden_size, self.output_size) # h by o                 # Random initialization of biases at hidden layer        self.b1 = np.random.randn(1, self.hidden_size)                # Random initialization of biases at output layer        self.b2 = np.random.randn(1, self.output_size)            def feed_forward(self, X):                '''        Description:            Forward pass of NN                Inputs:            X: np.ndarray(shape=(n, p), dtype=float)                training samples                Outputs:            output: np.ndarray(shape=(n, output_size), dtype=float)        '''                # Inputs to sigmoid at hidden layer for all training samples        z1 = (np.dot(X, self.W1)) + self.b1                # Output of sigmoid at hidden layer for all training samples        h1 = self.sigmoid(z1)                # Inputs to sigmoid at output layer for all training samples        z2 = (np.dot(h1, self.W2)) + self.b2                # Output of sigmoid at output layer        output = self.sigmoid(z2)                  return output            def sigmoid(self, s, deriv=False):                '''        Description:            Output of logistic sigmoid                Inputs:            s: float                input value            deriv: bool                indicates whether to get function output or derivative output                Outputs:            output: np.array(dtype=float)                output for all training samples        '''                if (deriv == True):            output = self.sigmoid(s) * (1 - self.sigmoid(s))        else:            output = 0.5 * (1 + np.tanh(s / 2))                    return output        def back_prop(self, X, y, output):                '''        Description:            Backward pass of NN to update weights/biases                Inputs:            X: np.ndarray(shape=(n, p), dtype=float)                training samples            y: np.ndarray(shape=(n, output_size), dtype=float)            output: np.ndarray(shape=(n, output_size), dtype=float)                probabilities for all classes                 Outputs:            N/A        '''                # Get output of sigmoid at hidden layer        z1 = (np.dot(X, self.W1)) + self.b1        h1 = self.sigmoid(z1)                # Get partial derivatives        dLdz2 = output - y        dLdW2 = h1.T.dot(dLdz2)        dLdb2 = np.mean(dLdz2, axis=0)        dLdz1 = dLdz2.dot(self.W2.T) * self.sigmoid(h1, deriv=True)        dLdW1 = X.T.dot(dLdz1)        dLdb1 = np.mean(dLdz1, axis=0)                # Update weights and biases        self.W1 = self.W1 - self.lr * dLdW1        self.W2 = self.W2 - self.lr * dLdW2        self.b1 = self.b1  - self.lrb * dLdb1        self.b2 = self.b2 - self.lrb * dLdb2            def TrainNetwork(self, X, y):                '''        Description:            Train for one epoch                Inputs:            X: np.ndarray(shape=(n, p), dtype=float)                training samples            y: np.ndarray(shape=(n, output_size), dtype=float)                Outputs:            output: np.ndarray(shape=(n, output_size), dtype=float)                probabilities for all classes        '''                # Calculate outputs of sigmoid at output layer        output = self.feed_forward(X)                # Perform back propogation to update weights/biases        self.back_prop(X, y, output)                return outputif __name__ == "__main__":        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay    import matplotlib.pyplot as plt    import pickle    import os        # Load data file    pwd = os.getcwd()    save_loc = os.path.join(pwd, 'nbc_data')    file_name = 'nbc_cat_data.pkl'    full_file = os.path.join(save_loc, file_name)    with open(full_file, 'rb') as input_file:        data_cat = pickle.load(input_file)        # Randomly get rid of some of the data because this is really slooooow    data_cat = data_cat.sample(n=10000)        # Separate labels and features    y = np.array(data_cat.loc[:, 'snowfall'], dtype=str).T    y = np.array([y]).T        y_str = np.array(data_cat.loc[:, 'snowfall'], dtype=str)    y = np.ones(len(y_str), dtype=float)    msk = y_str == '0'    y[msk] = 0    y = np.array([y]).T        X = data_cat.drop(['snowfall'], axis=1)    X = (X - X.mean()) / X.std()    X = np.array(X, dtype=int)        # Define inputs    input_size = X.shape[1]    output_size = 1    hidden_size = 50    n = len(X)    lr = 0.01    lrb = 0.01        NN_obj = NeuralNetwork(input_size, output_size, hidden_size, n, lr, lrb)        total_loss = []    avg_loss = []    epochs = 500        for i in range(epochs):         output = NN_obj.TrainNetwork(X, y)        output = np.where(output > 0.5, 1, 0)        total_loss.append(np.sum(np.square(output - y)))        avg_loss.append(np.mean(np.square(output - y)))        # Plot loss by epoch    fig = plt.figure()    ax = plt.axes()    x = np.linspace(0, epochs, epochs)    ax.plot(x, total_loss)    plt.xlabel('Epoch')    plt.ylabel('Total Loss')    plt.title('Loss By Epoch')    plt.grid()        # Plot confusion matrix with test data    with open(full_file, 'rb') as input_file:        data_cat = pickle.load(input_file)    data_cat = data_cat.sample(n=100000)    y = np.array(data_cat.loc[:, 'snowfall'], dtype=str).T    y = np.array([y]).T    y_str = np.array(data_cat.loc[:, 'snowfall'], dtype=str)    y = np.ones(len(y_str), dtype=float)    msk = y_str == '0'    y[msk] = 0    y = np.array([y]).T    X = data_cat.drop(['snowfall'], axis=1)    X = (X - X.mean()) / X.std()    X = np.array(X, dtype=float)    output = NN_obj.feed_forward(X)    output = np.where(output > 0.5, 1, 0)    cm = confusion_matrix(y, output)    ConfusionMatrixDisplay(cm).plot()                    