import os
import json
import numpy as np
import pandas as pd

# Set MLflow to use temp dir so tests don't fail on path issues
os.environ["MLFLOW_TRACKING_URI"] = "sqlite:///mlflow.db"
os.environ["MLFLOW_ARTIFACT_ROOT"] = "./mlartifacts"

from src.train import train


FEATURE_NAMES = [
    "age", "workclass", "education_num", "marital_status", "occupation",
    "relationship", "sex", "capital_gain", "capital_loss", "hours_per_week",
]


def _make_temp_data(tmp_path):
    """Tạo dataset nhỏ với cùng schema Adult để sử dụng trong test."""
    rng = np.random.default_rng(0)
    n = 200
    X = rng.random((n, len(FEATURE_NAMES)))
    y = rng.integers(0, 2, size=n)
    df = pd.DataFrame(X, columns=FEATURE_NAMES)
    df["target"] = y
    train_path = tmp_path / "train.csv"
    holdout_path = tmp_path / "holdout.csv"
    df.iloc[:160].to_csv(train_path, index=False)
    df.iloc[160:].to_csv(holdout_path, index=False)
    return str(train_path), str(holdout_path)


def test_train_returns_float(tmp_path):
    """Kiểm tra hàm train() trả về một số thực trong khoảng [0, 1]."""
    train_path, eval_path = _make_temp_data(tmp_path)
    result = train(
        {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
        data_path=train_path,
        eval_path=eval_path,
    )
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


def test_report_file_created(tmp_path):
    """Kiểm tra file outputs/report.json được tạo sau khi huấn luyện."""
    train_path, eval_path = _make_temp_data(tmp_path)
    # Change to tmp_path so outputs go there
    original_dir = os.getcwd()
    try:
        os.chdir(tmp_path)
        train(
            {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
            data_path=train_path,
            eval_path=eval_path,
        )
        report_path = "outputs/report.json"
        assert os.path.exists(report_path), "outputs/report.json not found"
        with open(report_path) as f:
            report = json.load(f)
        assert "f1_score" in report
        assert "accuracy" in report
    finally:
        os.chdir(original_dir)


def test_model_file_created(tmp_path):
    """Kiểm tra file models/model.joblib được tạo sau khi huấn luyện."""
    train_path, eval_path = _make_temp_data(tmp_path)
    original_dir = os.getcwd()
    try:
        os.chdir(tmp_path)
        train(
            {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
            data_path=train_path,
            eval_path=eval_path,
        )
        model_path = "models/model.joblib"
        assert os.path.exists(model_path), "models/model.joblib not found"
    finally:
        os.chdir(original_dir)
