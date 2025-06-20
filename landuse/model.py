# model.py
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import HistGradientBoostingClassifier

# Базовые параметры для всех моделей
BASE_PARAMS = {
    "random_state": 42,
    "n_jobs": -1
}

# Специфичные параметры для каждой модели
MODEL_PARAMS = {
    "rf": {
        "n_estimators": 200,
        "max_depth": 7,
        "class_weight": "balanced",
        **BASE_PARAMS
    },
    "xgb": {
        "n_estimators": 200,
        "max_depth": 7,
        "learning_rate": 0.05,
        "scale_pos_weight": 1,  # Аналог class_weight для XGBoost
        **BASE_PARAMS
    },
    "lgb": {
        "n_estimators": 200,
        "max_depth": 7,
        "learning_rate": 0.05,
        "class_weight": "balanced",
        **BASE_PARAMS
    },
    "cb": {
        "iterations": 200,  # CatBoost использует iterations вместо n_estimators
        "depth": 7,
        "learning_rate": 0.05,
        "thread_count": -1,  # Аналог n_jobs для CatBoost
        "auto_class_weights": "Balanced",
        "random_seed": 42
    },
    "hgb": {
        "max_iter": 200,
        "max_depth": 7,
        "learning_rate": 0.05,
        "random_state": 42
    }
}

def get_model_params(model_name):
    """Возвращает параметры для конкретной модели, обрабатывая специфичные случаи"""
    params = MODEL_PARAMS.get(model_name, {}).copy()
    
    # Особые случаи
    if model_name == 'xgb':
        params['n_jobs'] = params.get('n_jobs', -1)
    elif model_name == 'cb':
        params.pop('n_jobs', None)  # Удаляем n_jobs для CatBoost
        
    return params

def build_model():
    # Инициализация моделей с их параметрами
    models = [
        ('rf', RandomForestClassifier(**get_model_params('rf'))),
        ('xgb', XGBClassifier(**get_model_params('xgb'))),
        ('lgb', LGBMClassifier(**get_model_params('lgb'))),
        ('cb', CatBoostClassifier(**get_model_params('cb'))),
        ('hgb', HistGradientBoostingClassifier(**get_model_params('hgb')))
    ]

    voting_clf = VotingClassifier(
        estimators=models,
        voting='soft',
        n_jobs=-1
    )

    pipeline = ImbPipeline([
        ('scaler', StandardScaler()),
        ('smote', SMOTE(random_state=42)),
        ('clf', voting_clf)
    ])
    
    return pipeline