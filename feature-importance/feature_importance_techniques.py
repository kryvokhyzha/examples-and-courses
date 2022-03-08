from typing import Callable
from collections.abc import Iterable

import shap
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import log_loss, accuracy_score, f1_score
from sklearn.model_selection._split import _BaseKFold, StratifiedKFold


def cv_score(clf, X, y, scoring: Callable = accuracy_score, cv: _BaseKFold = None, **fit_params):
    fold = 1
    scores = []
    for train_index, test_index in cv.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = clf.fit(X_train, y_train, **fit_params)
        y_pred = model.predict(X_test)
        f1 = scoring(y_pred, y_test)
        print("FOLD:", fold, "SCORE:", f1)
        fold += 1
        scores.append(f1)
    return np.array(scores)


def single_feature_importance(features_names, clf, X, y, scoring, cv):
    imp = pd.DataFrame(columns=["mean", "std"])
    for feature_name in features_names:
        df0 = cv_score(clf, X=X[[feature_name]], y=y, scoring=scoring, cv=cv)
        imp.loc[feature_name, "mean"] = df0.mean()
        imp.loc[feature_name, "std"] = df0.std() * df0.shape[0] ** -0.5
    return imp


def feature_importance_MDI(fit, features_names: Iterable):
    # feat importance based on IS mean impurity reduction
    if hasattr(fit, "estimators_"):
        df0 = {i: tree.feature_importances_ for i, tree in enumerate(fit.estimators_)}
        df0 = pd.DataFrame.from_dict(df0, orient="index")
        df0.columns = features_names
        df0 = df0.replace(0, np.nan)  # because max_features=1
        imp = pd.concat({"mean": df0.mean(), "std": df0.std() * df0.shape[0] ** -0.5}, axis=1)
        imp /= imp["mean"].sum()
    elif hasattr(fit, "feature_importances_"):
        imp = pd.Series(fit.feature_importances_, index=features_names).to_frame(name="mean")
        imp["std"] = np.NAN
    return imp


def feature_importance_MDA(clf, X: pd.DataFrame, y: pd.Series, cv: _BaseKFold, scoring: Callable = accuracy_score):
    scr0, scr1 = pd.Series(), pd.DataFrame(columns=X.columns)
    for i, (train, test) in enumerate(cv.split(X=X, y=y)):
        X0, y0 = X.iloc[train, :], y.iloc[train]
        X1, y1 = X.iloc[test, :], y.iloc[test]
        fit = clf.fit(X=X0, y=y0)
        if scoring == log_loss:
            prob = fit.predict_proba(X1)
            scr0.loc[i] = scoring(y1, prob, labels=clf.classes_)
        else:
            pred = fit.predict(X1)
            scr0.loc[i] = scoring(y1, pred)
        for j in X.columns:
            X1_ = X1.copy(deep=True)
            np.random.shuffle(X1_[j].values)  # permutation of a single column
            if scoring == log_loss:
                prob = fit.predict_proba(X1_)
                scr1.loc[i, j] = scoring(y1, prob, labels=clf.classes_)
            else:
                pred = fit.predict(X1_)
                scr1.loc[i, j] = scoring(y1, pred)
    imp = (-scr1).add(scr0, axis=0)
    if scoring == "neg_log_loss":
        imp = imp / -scr1
    else:
        imp = imp / (1.0 - scr1)
    imp = pd.concat({"mean": imp.mean(), "std": imp.std() * imp.shape[0] ** -0.5}, axis=1)
    return imp, scr0.mean()


def feature_importance_CFI_MDA(
    X,
    y,
    clf,
    cv,
    scoring=accuracy_score,
    C=2,
    epsilon=1e-5,
):
    def correlDist(corr):
        # A distance matrix based on correlation, where 0<=d[i,j]<=1
        # This is a proper distance metric
        dist = ((1 - corr) / 2.0) ** 0.5  # distance matrix
        return dist

    def cluster_features():
        dist_matrix = correlDist(X.corr())
        dist_matrix = dist_matrix.fillna(epsilon)
        link = linkage(dist_matrix, method="ward")
        clusters = fcluster(link, t=C, criterion="maxclust")
        return clusters

    def feat_imp_MDA_clusterized(clf, X, y, cv, scoring, cluster_subsets):
        # feat importance based on OOS score reduction
        scr0, scr1 = pd.Series(), pd.DataFrame(columns=X.columns)

        for i, (train, test) in enumerate(cv.split(X=X, y=y)):
            X0, y0 = X.iloc[train, :], y.iloc[train]
            X1, y1 = X.iloc[test, :], y.iloc[test]
            fit = clf.fit(X=X0, y=y0)
            if scoring == log_loss:
                pred = fit.predict_proba(X1)
                scr0.loc[i] = scoring(y1, pred)
            else:
                pred = fit.predict(X1)
                scr0.loc[i] = scoring(y1, pred)
            # for j in X.columns:
            for j in cluster_subsets:

                X1_ = X1.copy(deep=True)

                for ji in j:
                    np.random.shuffle(X1_[ji].values)  # permutation of a single column
                if scoring == log_loss:
                    pred = fit.predict_proba(X1_)
                    scr1.loc[i, j] = scoring(y1, pred)
                else:
                    pred = fit.predict(X1_)
                    scr1.loc[i, j] = scoring(y1, pred)

        imp = (-scr1).add(scr0, axis=0)
        imp = imp / (1.0 - scr1)
        imp = pd.concat({"mean": imp.mean(), "std": imp.std() * imp.shape[0] ** -0.5}, axis=1)
        return imp, scr0.mean()

    clusters = cluster_features()
    cluster_subsets = [[f for c, f in zip(clusters, X.columns) if c == ci] for ci in range(1, C + 1)]

    fit = clf.fit(X=X, y=y)
    imp, oos = feat_imp_MDA_clusterized(clf, X, y, cv, scoring, cluster_subsets)
    return imp, oos


def SHAP_importance(clf, X):
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X)
    fi0 = np.abs(shap_values[0]).mean(axis=0)
    fi1 = np.abs(shap_values[1]).mean(axis=0)
    fi = fi0 + fi1
    imp = pd.DataFrame({"feature": X.columns.tolist(), "mean": fi})
    imp = imp.set_index("feature")
    return imp


def feature_importance(X, y, cv, scoring=accuracy_score, method="SFI", clf=RandomForestClassifier()):
    fit = clf.fit(X=X, y=y)
    if method == "MDI":
        imp = feature_importance_MDI(fit, features_names=X.columns)
        oos = cv_score(clf, X, y, cv=cv, scoring=scoring).mean()
    elif method == "MDA":
        imp, oos = feature_importance_MDA(clf, X, y, cv=cv, scoring=scoring)
    elif method == "SFI":
        oos = cv_score(clf, X, y, cv=cv, scoring=scoring).mean()
        imp = single_feature_importance(X.columns, clf, X, y, scoring=scoring, cv=cv)
    elif method == "CFI":
        C = 3
        imp, oos = feature_importance_CFI_MDA(X, y, clf, cv, scoring, C)
    elif method == "SHAP":
        imp = SHAP_importance(clf, X)
        oos = None
    elif method == "MI":
        mutual_imp = mutual_info_classif(X, y)
        mutual_imp = pd.Series(mutual_imp, index=list(X.columns))
        oos = None
        imp = pd.DataFrame(index=list(X.columns))
        imp["mean"] = mutual_imp
        imp["std"] = mutual_imp
    return imp, oos


def compute_feature_importance(
    X: pd.DataFrame,
    y: pd.Series,
    cv: _BaseKFold,
    scoring: Callable = accuracy_score,
    methods: list = ["MDA", "MDI", "SFI"],
    clf=RandomForestClassifier(),
):

    importances = []
    out = []

    for method in methods:
        imp, oos = feature_importance(
            X=X,
            y=y,
            cv=cv,
            scoring=scoring,
            clf=clf,
            method=method,
        )
        importances.append(imp)
        df0 = imp[["mean"]] / imp["mean"].abs().sum()
        df0["type"] = df0.index
        df0 = df0.groupby("type")["mean"].sum().to_dict()
        df0.update({"oos": oos})
        out.append(df0)
        out_csv = pd.DataFrame(out)
        out_csv.to_csv("stats.csv")
    out_csv["method"] = methods
    out_csv.set_index("method")
    return out_csv, importances
