import numpy as npclass NeuralNetwork():        def __init__(self, input_size, output_size, hidden_size, n, lr, lrb):                '''        Description:            Initialize feed forward NN class                Inputs:            input_size: int                number of inputs            output_size: int                number of outputs            hidden_size: int                number of nodes in single hidden layer            n: int                number of training samples            lr: float                learning rate for weights            lrb: float                learning rate for biases                    Outputs:            N/A        '''                self.input_size = input_size        self.output_size = output_size        self.hidden_size = hidden_size        self.n = n        self.lr = lr        self.lrb = lrb                # Random initialization of weights from input layer to hidden layer        self.W1 = np.random.randn(self.input_size, self.hidden_size) # c by h                 # Random initialization of weights from hidden layer to output layer        self.W2 = np.random.randn(self.hidden_size, self.output_size) # h by o                 # Random initialization of biases at hidden layer        self.b1 = np.random.randn(1, self.hidden_size)                # Random initialization of biases at output layer        self.b2 = np.random.randn(1, self.output_size)            def sigmoid(self, s, deriv=False):                '''        Description:            Output of logistic sigmoid                Inputs:            s: float                input value            deriv: bool                indicates whether to get function output or derivative output                Outputs:            output: np.array(dtype=float)                output for all training samples        '''                if (deriv == True):            output = self.sigmoid(s) * (1 - self.sigmoid(s))        else:            output = 0.5 * (1 + np.tanh(s / 2))                    return output        def softmax(self, s, deriv=False):                '''        Description:            Output of softmax                Inputs:            s: float                input value            deriv: bool                indicates whether to get function output or derivative output                Outputs:            output: np.array(dtype=float)                output for all training samples        '''                if (deriv == True):            output = self.softmax(s) * (1 - self.softmax(s))        else:            max_s = np.max(s, axis=1, keepdims=True)            exp_s = np.exp(s - max_s)            sum_exp_s = np.sum(exp_s, axis=1, keepdims=True)            output = exp_s / sum_exp_s                    return output        def feed_forward(self, X):                '''        Description:            Forward pass of NN                Inputs:            X: np.ndarray(shape=(n, p), dtype=float)                training samples                Outputs:            output: np.ndarray(shape=(n, output_size), dtype=float)        '''                # Inputs to sigmoid at hidden layer for all training samples        z1 = (np.dot(X, self.W1)) + self.b1                # Output of sigmoid at hidden layer for all training samples        h1 = self.sigmoid(z1)                # Inputs to sigmoid at output layer for all training samples        z2 = (np.dot(h1, self.W2)) + self.b2                # Output of softmax at output layer        output = self.softmax(z2)                  return output        def back_prop(self, X, y, output):                '''        Description:            Backward pass of NN to update weights/biases                Inputs:            X: np.ndarray(shape=(n, p), dtype=float)                training samples            y: np.ndarray(shape=(n, output_size), dtype=float)            output: np.ndarray(shape=(n, output_size), dtype=float)                probabilities for all classes                 Outputs:            N/A        '''                # Get output of sigmoid at hidden layer        z1 = (np.dot(X, self.W1)) + self.b1        h1 = self.sigmoid(z1)                # Get partial derivatives        dLdz2 = output - y        dLdW2 = h1.T.dot(dLdz2)        dLdb2 = np.mean(dLdz2, axis=0)        dLdz1 = dLdz2.dot(self.W2.T) * self.sigmoid(h1, deriv=True)        dLdW1 = X.T.dot(dLdz1)        dLdb1 = np.mean(dLdz1, axis=0)                # Update weights and biases        self.W1 = self.W1 - self.lr * dLdW1        self.W2 = self.W2 - self.lr * dLdW2        self.b1 = self.b1  - self.lrb * dLdb1        self.b2 = self.b2 - self.lrb * dLdb2            def TrainNetwork(self, X, y):                '''        Description:            Train for one epoch                Inputs:            X: np.ndarray(shape=(n, p), dtype=float)                training samples            y: np.ndarray(shape=(n, output_size), dtype=float)                Outputs:            output: np.ndarray(shape=(n, output_size), dtype=float)                probabilities for all classes        '''                # Calculate outputs of sigmoid at output layer        output = self.feed_forward(X)                # Perform back propogation to update weights/biases        self.back_prop(X, y, output)                return outputif __name__ == "__main__":        from sklearn.metrics import confusion_matrix    import matplotlib.pyplot as plt    import pickle    import os    import seaborn as sns    from sklearn.model_selection import train_test_split    from imblearn.under_sampling import RandomUnderSampler    import tensorflow as tf        # Load data file    pwd = os.getcwd()    save_loc = os.path.join(pwd, 'nbc_data')    file_name = 'nbc_cat_data.pkl'    full_file = os.path.join(save_loc, file_name)    with open(full_file, 'rb') as input_file:        data_cat = pickle.load(input_file)        # Separate labels and features    y = np.array(data_cat.loc[:, 'snowfall'], dtype=str).T    y = np.array([y]).T    X = data_cat.drop(['snowfall'], axis=1)    X = (X - X.mean()) / X.std()    X = np.array(X, dtype=float)        # Separate test and train data    X_train, X_test, y_train, y_test = train_test_split(X, y,        test_size=0.3, random_state=42)        # We would like a balanced dataset - make equal labels with undersampling    under_sampler = RandomUnderSampler(sampling_strategy='majority')    X_train, y_train = under_sampler.fit_resample(X_train, y_train)    y_train = np.array([y_train]).T        # Define inputs    input_size = X.shape[1]    output_size = len(np.unique(y))    hidden_size = 500    n = len(X_train)    lr = 0.0001    lrb = 0.0001        # Need one-hot labels for y_train    enum = enumerate(np.unique(y))    d = dict((i,j) for i, j in enum)    one_hot_labels = np.zeros((n, output_size))    for i in range(n):        val = y_train[i][0]        idx = list(d.values()).index(val)        one_hot_labels[i, idx] = 1        y_train_one_hot = one_hot_labels        # Need one-hot labels for y_test    enum = enumerate(np.unique(y))    d = dict((i,j) for i, j in enum)    one_hot_labels = np.zeros((len(X_test), output_size))    for i in range(n):        val = y_test[i][0]        idx = list(d.values()).index(val)        one_hot_labels[i, idx] = 1        y_test_one_hot = one_hot_labels        NN_obj = NeuralNetwork(input_size, output_size, hidden_size, n, lr, lrb)        total_loss = []    epochs = 500    loss_fn = tf.keras.losses.CategoricalCrossentropy()        for i in range(epochs):         print(i)        output = NN_obj.TrainNetwork(X_train, y_train_one_hot)        loss = loss_fn(y_train_one_hot, output).numpy()        total_loss.append(loss)        # Place to save figs    pwd = os.getcwd()    save_loc = os.path.join(pwd, 'figs', 'NN')    if not os.path.isdir(save_loc):        os.mkdir(save_loc)        # Plot loss by epoch    fig = plt.figure()    ax = plt.axes()    x = np.linspace(0, epochs, epochs)    ax.plot(x, total_loss)    plt.xlabel('Epoch')    plt.ylabel('Total Loss')    plt.title('Loss By Epoch')    plt.grid()    file_name = 'hand_NN_loss.png'    plt.savefig(os.path.join(save_loc, file_name), dpi=300, bbox_inches='tight')        # Make confusion matrix with test data    names = np.unique(y)    pred_mat = NN_obj.feed_forward(X_test)    pred = []    for (i, row) in enumerate(pred_mat):        max_idx = np.argmax(row)        lab = d[max_idx]        pred.append(lab)    truth = y_test    confuse = confusion_matrix(truth, pred)    confuse = confuse.astype('float')    for (i, r) in enumerate(confuse):        confuse[i] = r / sum(r)    plt.figure(figsize=(20, 20))    fx = sns.heatmap(confuse, annot=True, fmt='.2f', cmap='GnBu')    fx.set_title('Confusion Matrix \n');    fx.set_xlabel('\n Predicted Values\n')    fx.set_ylabel('Actual Values\n');    fx.xaxis.set_ticklabels(names)    fx.yaxis.set_ticklabels(names)    file_name = 'hand_NN_confusion.png'    plt.savefig(os.path.join(save_loc, file_name), dpi=300, bbox_inches='tight')                