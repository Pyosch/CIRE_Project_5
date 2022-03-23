import numpy as np
import pandas as pd
from sklearn import datasets, linear_model, model_selection, metrics


def create_energy_predict_model(verbose):
    data = pd.read_csv('output.csv')
    np.set_printoptions(threshold=np.inf) # display entire array

    attr_cols = ['Timeslot', 'Weekday',\
                 'CA1_H-1','CP1_H-1', 'CA2_H-1', 'CP2_H-1', 'CA3_H-1', 'CP3_H-1', 'CA4_H-1', 'CP4_H-1', 'CA5_H-1',\
                 'CP5_H-1', 'CA6_H-1', 'CP6_H-1', 'CA7_H-1', 'CP7_H-1', 'CA8_H-1', 'CP8_H-1', 'CA9_H-1', 'CP9_H-1',\
                 'CA10_H-1', 'CP10_H-1', 'CA11_H-1', 'CP11_H-1', 'CA12_H-1', 'CP12_H-1', 'CA13_H-1', 'CP13_H-1',\
                 'CA14_H-1', 'CP14_H-1', 'CA15_H-1', 'CP15_H-1', 'CA16_H-1', 'CP16_H-1', 'CA17_H-1', 'CP17_H-1',\
                 'CA18_H-1', 'CP18_H-1', 'CA19_H-1', 'CP19_H-1', 'CA20_H-1', 'CP20_H-1', 'CA21_H-1', 'CP21_H-1',\
                 'CA22_H-1', 'CP22_H-1', 'CA23_H-1', 'CP23_H-1', 'CA24_H-1', 'CP24_H-1',\
                 'CA1_D-1', 'CP1_D-1', 'CA2_D-1', 'CP2_D-1', 'CA3_D-1', 'CP3_D-1', 'CA4_D-1', 'CP4_D-1', 'CA5_D-1',\
                 'CP5_D-1', 'CA6_D-1', 'CP6_D-1', 'CA7_D-1', 'CP7_D-1', 'CA8_D-1', 'CP8_D-1', 'CA9_D-1', 'CP9_D-1',\
                 'CA10_D-1', 'CP10_D-1', 'CA11_D-1', 'CP11_D-1', 'CA12_D-1', 'CP12_D-1', 'CA13_D-1', 'CP13_D-1',\
                 'CA14_D-1', 'CP14_D-1', 'CA15_D-1', 'CP15_D-1', 'CA16_D-1', 'CP16_D-1', 'CA17_D-1', 'CP17_D-1',\
                 'CA18_D-1', 'CP18_D-1', 'CA19_D-1', 'CP19_D-1', 'CA20_D-1', 'CP20_D-1', 'CA21_D-1', 'CP21_D-1',\
                 'CA22_D-1', 'CP22_D-1', 'CA23_D-1', 'CP23_D-1', 'CA24_D-1', 'CP24_D-1',\
                 'CA1_W-1', 'CP1_W-1', 'CA2_W-1', 'CP2_W-1', 'CA3_W-1', 'CP3_W-1', 'CA4_W-1', 'CP4_W-1', 'CA5_W-1',\
                 'CP5_W-1', 'CA6_W-1', 'CP6_W-1', 'CA7_W-1', 'CP7_W-1', 'CA8_W-1', 'CP8_W-1', 'CA9_W-1', 'CP9_W-1',\
                 'CA10_W-1', 'CP10_W-1', 'CA11_W-1', 'CP11_W-1', 'CA12_W-1', 'CP12_W-1', 'CA13_W-1', 'CP13_W-1',\
                 'CA14_W-1', 'CP14_W-1', 'CA15_W-1', 'CP15_W-1', 'CA16_W-1', 'CP16_W-1', 'CA17_W-1', 'CP17_W-1',\
                 'CA18_W-1', 'CP18_W-1', 'CA19_W-1', 'CP19_W-1', 'CA20_W-1', 'CP20_W-1', 'CA21_W-1', 'CP21_W-1',\
                 'CA22_W-1', 'CP22_W-1', 'CA23_W-1', 'CP23_W-1', 'CA24_W-1', 'CP24_W-1']
    
    #attr_cols = ["Timeslot","WeekDay","CA24","CP24","T24","WS24","CA23","CP23","T23","WS23","CA22","CP22","T22","WS22","CA21","CP21","T21","WS21","CA20","CP20","T20","WS20","CA19","CP19","T19","WS19","CA18","CP18","T18","WS18","CA17","CP17","T17","WS17","CA16","CP16","T16","WS16","CA15","CP15","T15","WS15","CA14","CP14","T14","WS14","CA13","CP13","T13","WS13","CA12","CP12","T12","WS12","CA11","CP11","T11","WS11","CA10","CP10","T10","WS10","CA9","CP9","T9","WS9","CA8","CP8","T8","WS8","CA7","CP7","T7","WS7","CA6","CP6","T6","WS6","CA5","CP5","T5","WS5","CA4","CP4","T4","WS4","CA3","CP3","T3","WS3","CA2","CP2","T2","WS2","CA1","CP1","T1","WS1","CT","CWS","PCA1","PCP1","PCA2","PCP2","PCA3","PCP3","PCA4","PCP4","PCA5","PCP5","PCA6","PCP6","PCA7","PCP7","PCA8","PCP8","PCA9","PCP9","PCA10","PCP10","PCA11","PCP11","PCA12","PCP12","PCA13","PCP13","PCA14","PCP14","PCA15","PCP15","PCA16","PCP16","PCA17","PCP17","PCA18","PCP18","PCA19","PCP19","PCA20","PCP20","PCA21","PCP21","PCA22","PCP22","PCA23","PCP23","PCA24","PCP24","TF1","WSF1","TF2","WSF2","TF3","WSF3","TF4","WSF4","TF5","WSF5","TF6","WSF6","TF7","WSF7","TF8","WSF8","TF9","WSF9","TF10","WSF10","TF11","WSF11","TF12","WSF12","TF13","WSF13","TF14","WSF14","TF15","WSF15","TF16","WSF16","TF17","WSF17","TF18","WSF18","TF19","WSF19","TF20","WSF20","TF21","WSF21","TF22","WSF22","TF23","WSF23","TF24","WSF24"]
    x = data[attr_cols].values
    
    predict_cols = ['CA1', 'CA2', 'CA3', 'CA4', 'CA5', 'CA6', 'CA7', 'CA8', 'CA9', 'CA10', 'CA11', 'CA12', 'CA13',\
                    'CA14', 'CA15', 'CA16', 'CA17', 'CA18', 'CA19', 'CA20', 'CA21', 'CA22', 'CA23', 'CA24']
    #predict_cols = ["TCP1","TCP2","TCP3","TCP4","TCP5","TCP6","TCP7","TCP8","TCP9","TCP10","TCP11","TCP12",\
    #                "TCP13","TCP14","TCP15","TCP16","TCP17","TCP18","TCP19","TCP20","TCP21","TCP22","TCP23","TCP24"]
    y = data[predict_cols].values
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.3)

    regressor = linear_model.LinearRegression()

    regressor.fit(x_train, y_train)

    if verbose:
        print("---ENERGY PREDICTION MODEL---")
        y_pred = regressor.predict(x_test)
        df = pd.DataFrame({'Actual': y_test.flatten(),
                           'Predicted': y_pred.flatten()})
        print(df)
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(
            metrics.mean_squared_error(y_test, y_pred)))

    return regressor

def create_price_predict_model(verbose):
    data = pd.read_csv('D:/Powertac/finals-2021/data/output.csv')
    #data = pd.read_csv('data.csv')
    np.set_printoptions(threshold=np.inf) # display entire array

    attr_cols = ['Timeslot', 'Weekday',\
                 'CA1_H-1','CP1_H-1', 'CA2_H-1', 'CP2_H-1', 'CA3_H-1', 'CP3_H-1', 'CA4_H-1', 'CP4_H-1', 'CA5_H-1',\
                 'CP5_H-1', 'CA6_H-1', 'CP6_H-1', 'CA7_H-1', 'CP7_H-1', 'CA8_H-1', 'CP8_H-1', 'CA9_H-1', 'CP9_H-1',\
                 'CA10_H-1', 'CP10_H-1', 'CA11_H-1', 'CP11_H-1', 'CA12_H-1', 'CP12_H-1', 'CA13_H-1', 'CP13_H-1',\
                 'CA14_H-1', 'CP14_H-1', 'CA15_H-1', 'CP15_H-1', 'CA16_H-1', 'CP16_H-1', 'CA17_H-1', 'CP17_H-1',\
                 'CA18_H-1', 'CP18_H-1', 'CA19_H-1', 'CP19_H-1', 'CA20_H-1', 'CP20_H-1', 'CA21_H-1', 'CP21_H-1',\
                 'CA22_H-1', 'CP22_H-1', 'CA23_H-1', 'CP23_H-1', 'CA24_H-1', 'CP24_H-1',\
                 'CA1_D-1', 'CP1_D-1', 'CA2_D-1', 'CP2_D-1', 'CA3_D-1', 'CP3_D-1', 'CA4_D-1', 'CP4_D-1', 'CA5_D-1',\
                 'CP5_D-1', 'CA6_D-1', 'CP6_D-1', 'CA7_D-1', 'CP7_D-1', 'CA8_D-1', 'CP8_D-1', 'CA9_D-1', 'CP9_D-1',\
                 'CA10_D-1', 'CP10_D-1', 'CA11_D-1', 'CP11_D-1', 'CA12_D-1', 'CP12_D-1', 'CA13_D-1', 'CP13_D-1',\
                 'CA14_D-1', 'CP14_D-1', 'CA15_D-1', 'CP15_D-1', 'CA16_D-1', 'CP16_D-1', 'CA17_D-1', 'CP17_D-1',\
                 'CA18_D-1', 'CP18_D-1', 'CA19_D-1', 'CP19_D-1', 'CA20_D-1', 'CP20_D-1', 'CA21_D-1', 'CP21_D-1',\
                 'CA22_D-1', 'CP22_D-1', 'CA23_D-1', 'CP23_D-1', 'CA24_D-1', 'CP24_D-1',\
                 'CA1_W-1', 'CP1_W-1', 'CA2_W-1', 'CP2_W-1', 'CA3_W-1', 'CP3_W-1', 'CA4_W-1', 'CP4_W-1', 'CA5_W-1',\
                 'CP5_W-1', 'CA6_W-1', 'CP6_W-1', 'CA7_W-1', 'CP7_W-1', 'CA8_W-1', 'CP8_W-1', 'CA9_W-1', 'CP9_W-1',\
                 'CA10_W-1', 'CP10_W-1', 'CA11_W-1', 'CP11_W-1', 'CA12_W-1', 'CP12_W-1', 'CA13_W-1', 'CP13_W-1',\
                 'CA14_W-1', 'CP14_W-1', 'CA15_W-1', 'CP15_W-1', 'CA16_W-1', 'CP16_W-1', 'CA17_W-1', 'CP17_W-1',\
                 'CA18_W-1', 'CP18_W-1', 'CA19_W-1', 'CP19_W-1', 'CA20_W-1', 'CP20_W-1', 'CA21_W-1', 'CP21_W-1',\
                 'CA22_W-1', 'CP22_W-1', 'CA23_W-1', 'CP23_W-1', 'CA24_W-1', 'CP24_W-1']
    
    #attr_cols = ["Timeslot","WeekDay","CA24","CP24","T24","WS24","CA23","CP23","T23","WS23","CA22","CP22","T22","WS22","CA21","CP21","T21","WS21","CA20","CP20","T20","WS20","CA19","CP19","T19","WS19","CA18","CP18","T18","WS18","CA17","CP17","T17","WS17","CA16","CP16","T16","WS16","CA15","CP15","T15","WS15","CA14","CP14","T14","WS14","CA13","CP13","T13","WS13","CA12","CP12","T12","WS12","CA11","CP11","T11","WS11","CA10","CP10","T10","WS10","CA9","CP9","T9","WS9","CA8","CP8","T8","WS8","CA7","CP7","T7","WS7","CA6","CP6","T6","WS6","CA5","CP5","T5","WS5","CA4","CP4","T4","WS4","CA3","CP3","T3","WS3","CA2","CP2","T2","WS2","CA1","CP1","T1","WS1","CT","CWS","PCA1","PCP1","PCA2","PCP2","PCA3","PCP3","PCA4","PCP4","PCA5","PCP5","PCA6","PCP6","PCA7","PCP7","PCA8","PCP8","PCA9","PCP9","PCA10","PCP10","PCA11","PCP11","PCA12","PCP12","PCA13","PCP13","PCA14","PCP14","PCA15","PCP15","PCA16","PCP16","PCA17","PCP17","PCA18","PCP18","PCA19","PCP19","PCA20","PCP20","PCA21","PCP21","PCA22","PCP22","PCA23","PCP23","PCA24","PCP24","TF1","WSF1","TF2","WSF2","TF3","WSF3","TF4","WSF4","TF5","WSF5","TF6","WSF6","TF7","WSF7","TF8","WSF8","TF9","WSF9","TF10","WSF10","TF11","WSF11","TF12","WSF12","TF13","WSF13","TF14","WSF14","TF15","WSF15","TF16","WSF16","TF17","WSF17","TF18","WSF18","TF19","WSF19","TF20","WSF20","TF21","WSF21","TF22","WSF22","TF23","WSF23","TF24","WSF24"]
    x = data[attr_cols].values
    
    predict_cols = ['CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CP7', 'CP8', 'CP9', 'CP10', 'CP11', 'CP12', 'CP13',\
                    'CP14', 'CP15', 'CP16', 'CP17', 'CP18', 'CP19', 'CP20', 'CP21', 'CP22', 'CP23', 'CP24']
    #predict_cols = ["TCP1","TCP2","TCP3","TCP4","TCP5","TCP6","TCP7","TCP8","TCP9","TCP10","TCP11","TCP12",\
    #                "TCP13","TCP14","TCP15","TCP16","TCP17","TCP18","TCP19","TCP20","TCP21","TCP22","TCP23","TCP24"]
    y = data[predict_cols].values
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.3)

    regressor = linear_model.LinearRegression()
    regressor.fit(x_train, y_train)

    if verbose:
        print("---PRICE PREDICTION MODEL---")
        y_pred = regressor.predict(x_test)
        df = pd.DataFrame({'Actual': y_test.flatten(),
                           'Predicted': y_pred.flatten()})
        print(df)
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(
            metrics.mean_squared_error(y_test, y_pred)))

    return regressor


def main():
    energy_model = create_energy_predict_model(verbose=True)
    price_model = create_price_predict_model(verbose=True)


if __name__ == "__main__":
    main()