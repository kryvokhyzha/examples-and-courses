from libs import *


def get_prediction(algorithm, X_train, X_test, y_train, y_test, cols, cf, threshold_plot=True) -> None:
    """
        Algorithm       - Algorithm used 
        cf              - ["coefficients","features"](`cooefficients` for logistic regression, `features` for tree based models)
        threshold_plot  - if True returns threshold plot for model

        Usage Example:
            model_building.get_prediction(lg, X_train, X_test, y_train, y_test, cols, "coefficients", threshold_plot=True)
    """
    # model
    algorithm.fit(X_train, y_train)
    predictions = algorithm.predict(X_test)
    probabilities = algorithm.predict_proba(X_test)

    # coeffs
    if cf == "coefficients":
        coefficients = pd.DataFrame(algorithm.coef_.ravel())
    elif cf == "features":
        coefficients = pd.DataFrame(algorithm.feature_importances_)
        
    column_df = pd.DataFrame(cols)
    coef_sumry = (pd.merge(coefficients, column_df, left_index=True,
                              right_index=True, how="left"))
    coef_sumry.columns = ["coefficients", "features"]
    coef_sumry = coef_sumry.sort_values(by="coefficients", ascending=False)
    
    print(algorithm)
    print("\n Classification report:\n", classification_report(y_test, predictions))
    print("Accuracy Score:", accuracy_score(y_test, predictions))

    # confusion matrix
    conf_matrix = confusion_matrix(y_test, predictions)
    # roc_auc_score
    model_roc_auc = roc_auc_score(y_test, predictions) 
    print("Area under curve:", model_roc_auc, "\n")
    fpr, tpr, thresholds = roc_curve(y_test, probabilities[:, 1])
    
    # plot confusion matrix
    trace1 = go.Heatmap(z=conf_matrix,
                        x=["0", "1"],
                        y=["0", "1"],
                        showscale=False,
                        colorscale="Picnic",
                        name="matrix")

    # plot roc curve
    trace2 = go.Scatter(x=fpr, y=tpr,
                        name="Roc: " + str(model_roc_auc),
                        line=dict(color=('rgb(22, 96, 167)'), width=2))
    trace3 = go.Scatter(x=[0, 1], y=[0, 1],
                        line=dict(color=('rgb(205, 12, 24)'), width=2,
                        dash='dot'))
    
    #plot coeffs
    trace4 = go.Bar(x=coef_sumry["features"], y=coef_sumry["coefficients"],
                    name="coefficients",
                    marker=dict(color=coef_sumry["coefficients"],
                                colorscale="Picnic",
                                line=dict(width=0.6, color="black")))

    #subplots
    fig = tls.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
                            subplot_titles=('Confusion Matrix',
                                            'Receiver operating characteristic',
                                            'Feature Importances'))
    
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 2)
    fig.append_trace(trace4, 2, 1)
    
    fig['layout'].update(showlegend=False, title="Model performance" ,
                         autosize=False, height=900, width=800,
                         plot_bgcolor='rgba(240,240,240, 0.95)',
                         paper_bgcolor='rgba(240,240,240, 0.95)',
                         margin=dict(b=195))
    fig["layout"]["xaxis2"].update(dict(title="false positive rate"))
    fig["layout"]["yaxis2"].update(dict(title="true positive rate"))
    fig["layout"]["xaxis3"].update(dict(showgrid=True, tickfont=dict(size=10),
                                        tickangle=90))
    py.iplot(fig)
    
    if threshold_plot: 
        visualizer = DiscriminationThreshold(algorithm)
        visualizer.fit(X_train, y_train)
        visualizer.poof()


def model_report(model, X_train, X_test, y_train, y_test, name) -> None:
    """
        Usage example:
            model1 = model_report(lg, X_train, X_test, y_train, y_test, "lg")
            model2 = model_report(dt, X_train, X_test, y_train, y_test, "dt")

            model_performances = pd.concat([model1, model2],axis = 0).reset_index()
            model_performances = model_performances.drop(columns = "index",axis =1)
            table  = ff.create_table(np.round(model_performances,4))
            py.iplot(table)
    """

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    recallscore = recall_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, predictions)
    f1score = f1_score(y_test, predictions) 
    kappa_metric = cohen_kappa_score(y_test, predictions)
    
    df = pd.DataFrame({"Model": [name],
                       "Accuracy_score": [accuracy],
                       "Recall_score": [recallscore],
                       "Precision": [precision],
                       "f1_score": [f1score],
                       "Area_under_curve": [roc_auc],
                       "Kappa_metric": [kappa_metric],
                      })
    return df


def error_metrics(y_true, y_preds, n, k) -> None:
    """
        1. Take y_true, y_preds, n, k.
            n is the number of observations.
            k is the number of independent variables, excluding the constant.
        2. Return 6 error metrics.
    """
    def r2_adj(y_true, y_preds, n, k):
        rss = np.sum((y_true - y_preds)**2)
        null_model = np.sum((y_true - np.mean(y_true))**2)
        r2 = 1 - rss/null_model
        r2_adj = 1 - ((1-r2)*(n-1))/(n-k-1)
        return r2_adj
    
    print('Mean Square Error: ', mean_squared_error(y_true, y_preds))
    print('Root Mean Square Error: ', np.sqrt(mean_squared_error(y_true, y_preds)))
    print('Mean absolute error: ', mean_absolute_error(y_true, y_preds))
    print('Median absolute error: ', median_absolute_error(y_true, y_preds))
    print('R^2 score:', r2_score(y_true, y_preds))
    print('Adjusted R^2 score:', r2_adj(y_true, y_preds, n, k))
