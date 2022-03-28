import numpy as np
import warnings
from sklearn.base import BaseEstimator

warnings.filterwarnings('ignore', category=RuntimeWarning)


def entropy(y):  
    """
    Computes entropy of the provided distribution. Use log(value + eps) for numerical stability
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, n_classes)
        One-hot representation of class labels for corresponding subset
    
    Returns
    -------
    float
        Entropy of the provided subset
    """
    EPS = 0.0005
    probs = np.mean(y, axis=0)
    
    return -(probs * np.log(probs + EPS)).sum()


def gini(y):
    """
    Computes the Gini impurity of the provided distribution
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, n_classes)
        One-hot representation of class labels for corresponding subset
    
    Returns
    -------
    float
        Gini impurity of the provided subset
    """
    probs = np.mean(y, axis=0)
    
    return 1 - np.power(probs, 2).sum()


def variance(y):
    """
    Computes the variance the provided target values subset
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, 1)
        Target values vector
    
    Returns
    -------
    float
        Variance of the provided target vector
    """
    
    return np.power(y - np.mean(y), 2).mean()


def mad_median(y):
    """
    Computes the mean absolute deviation from the median in the
    provided target values subset
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, 1)
        Target values vector
    
    Returns
    -------
    float
        Mean absolute deviation from the median in the provided vector
    """
    
    return np.abs(y - np.median(y)).mean()


def one_hot_encode(n_classes, y):
    y_one_hot = np.zeros((len(y), n_classes), dtype=float)
    y_one_hot[np.arange(len(y)), y.astype(int)[:, 0]] = 1.
    return y_one_hot


def one_hot_decode(y_one_hot):
    return y_one_hot.argmax(axis=1)[:, None]


class Node:
    """
    This class is provided "as is" and it is not mandatory to it use in your code.
    """
    def __init__(self, feature_index, threshold, proba=0):
        self.feature_index = feature_index
        self.value = threshold
        self.proba = proba
        self.left_child = None
        self.right_child = None
        
        
class DecisionTree(BaseEstimator):
    all_criterions = {
        'gini': (gini, True),  # (criterion, classification flag)
        'entropy': (entropy, True),
        'variance': (variance, False),
        'mad_median': (mad_median, False)
    }

    def __init__(
            self,
            n_classes=None,
            max_depth=np.inf,
            min_samples_split=2,
            bins=None,
            criterion_name='gini',
            threshold=0.5,
            debug=False,
    ):

        assert criterion_name in self.all_criterions.keys(), 'Criterion name must be on of the following: {}'.format(self.all_criterions.keys())
        
        self.n_classes = n_classes
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.bins = bins
        self.criterion_name = criterion_name
        self.threshold = threshold

        self.depth = 0
        self.root = None  # Use the Node class to initialize it later
        self.debug = debug

    def make_split(self, feature_index, threshold, X_subset, y_subset):
        """
        Makes split of the provided data subset and target values using provided feature and threshold
        
        Parameters
        ----------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels for corresponding subset
        
        Returns
        -------
        (X_left, y_left) : tuple of np.arrays of same type as input X_subset and y_subset
            Part of the providev subset where selected feature x^j < threshold
        (X_right, y_right) : tuple of np.arrays of same type as input X_subset and y_subset
            Part of the providev subset where selected feature x^j >= threshold
        """

        mask = X_subset[:, feature_index] < threshold
        X_left, y_left = X_subset[mask], y_subset[mask]
        X_right, y_right = X_subset[~mask], y_subset[~mask]
        
        return (X_left, y_left), (X_right, y_right)
    
    def make_split_only_y(self, feature_index, threshold, X_subset, y_subset):
        """
        Split only target values into two subsets with specified feature and threshold
        
        Parameters
        ----------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels for corresponding subset
        
        Returns
        -------
        y_left : np.array of type float with shape (n_objects_left, n_classes) in classification 
                   (n_objects, 1) in regression 
            Part of the provided subset where selected feature x^j < threshold

        y_right : np.array of type float with shape (n_objects_right, n_classes) in classification 
                   (n_objects, 1) in regression 
            Part of the provided subset where selected feature x^j >= threshold
        """

        mask = X_subset[:, feature_index] < threshold
        y_left, y_right = y_subset[mask], y_subset[~mask]
        
        return y_left, y_right

    def choose_best_split(self, X_subset, y_subset):
        """
        Greedily select the best feature and best threshold w.r.t. selected criterion
        
        Parameters
        ----------
        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels or target values for corresponding subset
        
        Returns
        -------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        """

        best_feature_index = None
        best_threshold = None
        best_split_criterion = -np.inf
        for feature_index in range(X_subset.shape[1]):
            if self.bins is None:
                thresholds = np.unique(X_subset[:, feature_index])
            else:
                thresholds = np.quantile(a=X_subset[:, feature_index], q=np.linspace(0, 1, self.bins))
                
            for threshold in thresholds:
                y_left, y_right = self.make_split_only_y(feature_index, threshold, X_subset, y_subset)
                # if len(y_left) > 0 and len(y_right) > 0:
                split_criterion = \
                    self.criterion(y_subset) - \
                    ((len(y_left) * self.criterion(y_left) + len(y_right) * self.criterion(y_right)) / len(y_subset))
                    
                # split_criterion = (len(y_left) * self.criterion(y_left) + len(y_right) * self.criterion(y_right)) / len(y_subset)

                if split_criterion > best_split_criterion:
                    best_feature_index = feature_index
                    best_threshold = threshold
                    best_split_criterion = split_criterion
        
        return best_feature_index, best_threshold
    
    def make_tree(self, X_subset, y_subset, depth):
        """
        Recursively builds the tree
        
        Parameters
        ----------
        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels or target values for corresponding subset
            
        depth : int
            Depth of current node
        
        Returns
        -------
        root_node : Node class instance
            Node of the root of the fitted tree
        """

        if (
            X_subset.shape[0] <= self.min_samples_split or
            depth >= self.max_depth
        ):
            new_node = Node(None, None)
            new_node.proba = np.mean(y_subset, axis=0)
            self.depth = max(depth, self.depth)
        else:
            feature_index, threshold = self.choose_best_split(X_subset, y_subset)
            new_node = Node(feature_index, threshold)
            (X_left, y_left), (X_right, y_right) = self.make_split(feature_index, threshold, X_subset, y_subset)

            if X_left.shape[0] == 0 or X_right.shape[0] == 0:
                new_node.feature_index = None
                new_node.value = None
                new_node.proba = np.mean(y_subset, axis=0)
            else:
                left_node = self.make_tree(X_left, y_left, depth+1)
                right_node = self.make_tree(X_right, y_right, depth+1)
                new_node.left_child = left_node
                new_node.right_child = right_node
                
        return new_node
        
    def fit(self, X, y):
        """
        Fit the model from scratch using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data to train on

        y : np.array of type int with shape (n_objects, 1) in classification 
                   of type float with shape (n_objects, 1) in regression 
            Column vector of class labels in classification or target values in regression
        
        """
        assert len(y.shape) == 2 and len(y) == len(X), 'Wrong y shape'
        self.criterion, self.classification = self.all_criterions[self.criterion_name]
        if self.classification:
            if self.n_classes is None:
                self.n_classes = len(np.unique(y))
            y = one_hot_encode(self.n_classes, y)

        self.root = self.make_tree(X, y, 0)

    def recursive_inference(self, X, node):
        """
        Recursively gets the prediction
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the test set

        node : Node
            Current Node in the decision tree
        
        Returns
        -------
        y : np.array of type int with shape (n_objects, num_classes) in classification 
                   of type float with shape (n_objects, 1) in regression
            Probabilities of each class for the provided objects in classification or predicted values in regression
        """
        
        if node.left_child is not None or node.right_child is not None:
            mask = X[:, node.feature_index] < node.value
            X_left, X_right = X[mask], X[~mask]
            
            y = np.full((X.shape[0], self.n_classes), [None]*self.n_classes) if self.classification else np.full(X.shape[0], None)
            y[mask] = self.recursive_inference(X_left, node.left_child)
            y[~mask] = self.recursive_inference(X_right, node.right_child)
            return y
        else:
            return np.full((X.shape[0], self.n_classes), node.proba) if self.classification else np.full(X.shape[0], node.proba)
    
    def predict(self, X):
        """
        Predict the target value or class label  the model from scratch using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data the predictions should be provided for

        Returns
        -------
        y_predicted : np.array of type int with shape (n_objects, 1) in classification 
                   (n_objects, 1) in regression 
            Column vector of class labels in classification or target values in regression
        
        """

        y_predicted = self.recursive_inference(X, self.root)
        if self.classification:
            if len(y_predicted.shape) == 2 and y_predicted.shape[1] > 1:
                y_predicted = np.argmax(y_predicted, axis=1)
            else:
                y_predicted = (y_predicted > self.threshold).astype(int)

        return y_predicted
        
    def predict_proba(self, X):
        """
        Only for classification
        Predict the class probabilities using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data the predictions should be provided for

        Returns
        -------
        y_predicted_probs : np.array of type float with shape (n_objects, n_classes)
            Probabilities of each class for the provided objects
        
        """
        assert self.classification, 'Available only for classification problem'

        y_predicted_probs = self.recursive_inference(X, self.root)
        
        return y_predicted_probs
