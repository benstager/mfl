import mfl as mfl
import pandas as pd
import numpy as np
import mfl.api.data_loaders as mfldata
import nfl_data_py as nfl

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, recall_score, precision_score, precision_recall_curve

from xgboost import XGBClassifier, XGBRFClassifier

from catboost import CatBoostClassifier

import keras
from keras.layers import Dense, ReLU, Bidirectional, Normalization, Dropout, Input
from keras.models import Sequential

import joblib

ALL_MODELS = os.listdir("../saved_models/")

class FranchiseQB:
    def __init__(self, 
                 feature_set='numeric', 
                 model='catboost', 
                 dataset='../data/for_modeling.csv', 
                 **kwargs):
        
        self.feature_set = feature_set
        self.model = model 
        self.dataset = dataset
        self.kwargs = kwargs
        self.model_map = {
            'catboost' : CatBoostClassifier(),
            'xgb' : XGBClassifier(), 
            'rf' : RandomForestClassifier(),
            'lr' : LogisticRegression(),
            'hgb' : HistGradientBoostingClassifier(),
            'svm' : SVC(),
            'nn_basic': ...
        }
        self.available_models = list(self.model_map.keys())
        self.model_func = self.model_map[model]
        self.full_dataset = pd.read_csv(dataset)

    def create_training_data(self, n_splits=4, stratify=True):
        pass

    def map_response(self, x):
        if x >= 4:
            return 1
        else: 
            return 0
        
    def score(self, y_test, y_probs, y_preds):
        accuracy = accuracy_score(y_test, y_preds)
        f1 = f1_score(y_test, y_preds)
        roc_auc = roc_auc_score(y_test, y_probs)

        metric_dict = {
            'accuracy' : accuracy,
            'f1' : f1,
            'roc_auc': roc_auc
        }

        return metric_dict

    def catboost(self, feature_set=None, kfold=False, folds=2):
        self.feature_set = feature_set
        self.kfold = kfold
        self.folds = folds

        df = self.full_dataset.dropna()
        df = df[df['season'] <= 2019]

        if feature_set is None:
            X = df.drop(['pfr_player_name', 'seasons_with_draft_team', 'name'],axis=1)
            y = df['seasons_with_draft_team']
        elif feature_set is not None:
            pass
        

        self.X = X
        self.y = y
        self.y_mapped = y.apply(self.map_response)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, 
                                                                                self.y_mapped, 
                                                                                test_size=.25, 
                                                                                stratify=self.y_mapped, 
                                                                                shuffle=True)

        model = CatBoostClassifier(one_hot_max_size=5, 
                                   iterations=300, 
                                   cat_features=X.select_dtypes(include='object').columns.tolist())
        
        model.fit(self.X_train, self.y_train)

        self.y_preds = model.predict(self.X_test)
        self.y_probs = model.predict_proba(self.X_test)[:,1]

        metrics = self.score(self.y_test, self.y_probs, self.y_preds)
        
        model.fit(X, self.y_mapped)
        self.fit_model = model
        self.model_results = pd.DataFrame(metrics, index=[0])
        

    def predict_2025_qb(self, player_name, round, pick, recent_team, season=2020):
        
        name = player_name
        season = season
        
        variant_features = ['round', 'pick', 'season']
        available_features = np.setdiff1d(self.fit_model.feature_names_[:-1], variant_features).tolist()

        initial_features = pd.DataFrame({
            'round' : round,
            'pick' : pick,
            'season' : season
        }, index=[0])

        predictors = mfldata.scrape_NFL_REF_QB(player_name=player_name)[available_features]
        
        processing = pd.concat([initial_features, predictors], axis=1)
        processing['recent_team'] = recent_team

        return self.fit_model.predict_proba(processing)

