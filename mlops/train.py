import os
import time
from typing import Dict, Any, Tuple
import json
import pandas as pd
import numpy as np

# MLflow e scikit-learn
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split

def _load_dataset(dataset_path: str) -> pd.DataFrame:
    # Aceita caminhos absolutos e relativos
    path = dataset_path if os.path.isabs(dataset_path) else os.path.join(os.getcwd(), dataset_path.lstrip("/"))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset não encontrado em: {path}")

    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Aceita lista de itens ou dict com chave "data"
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        df = pd.DataFrame(data)
    elif ext == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Formato de dataset não suportado: {ext}. Use .json ou .csv.")

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset deve conter colunas 'text' e 'label'.")
    return df

def _prepare_data(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, TfidfVectorizer]:
    X_train, X_test, y_train, y_test = train_test_split(df["text"].values, df["label"].values, test_size=0.2, random_state=42, stratify=df["label"].values)
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    return X_train_vec, X_test_vec, y_train, y_test, vectorizer

def train_or_update_model(dataset_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Treinamento com MLflow:
    - Carrega dataset
    - Prepara features (TF-IDF)
    - Treina LogisticRegression
    - Loga params, métricas e modelo no MLflow
    """
    start_ts = time.time()

    # Defina experimento (cria se não existir)
    experiment_name = params.get("experiment_name", "faq-classifier")
    mlflow.set_experiment(experiment_name)

    # Parâmetros com defaults seguros
    lr_C = float(params.get("C", 1.0))
    lr_max_iter = int(params.get("max_iter", 200))
    lr_solver = str(params.get("solver", "liblinear"))

    # Carregar e preparar dados
    df = _load_dataset(dataset_path)
    X_train, X_test, y_train, y_test, vectorizer = _prepare_data(df)

    with mlflow.start_run() as run:
        run_id = run.info.run_id

        # Log de parâmetros
        mlflow.log_param("C", lr_C)
        mlflow.log_param("max_iter", lr_max_iter)
        mlflow.log_param("solver", lr_solver)
        mlflow.log_param("dataset_path", dataset_path)
        mlflow.log_param("n_train", len(y_train))
        mlflow.log_param("n_test", len(y_test))

        # Modelo
        model = LogisticRegression(C=lr_C, max_iter=lr_max_iter, solver=lr_solver)
        model.fit(X_train, y_train)

        # Métricas
        y_pred = model.predict(X_test)
        y_proba = None
        try:
            y_proba = model.predict_proba(X_test)
        except Exception:
            # Alguns solvers não expõem predict_proba para certas configurações
            pass

        acc = float(accuracy_score(y_test, y_pred))
        mlflow.log_metric("accuracy", acc)

        if y_proba is not None:
            try:
                ll = float(log_loss(y_test, y_proba))
                mlflow.log_metric("log_loss", ll)
            except Exception:
                ll = None
        else:
            ll = None

        # Log do vetorizer e modelo como artefatos
        # Salvamos um pipeline simples (vectorizer + coef do modelo)
        # Para produção, use joblib ou sklearn pipeline completo.
        import joblib
        artifacts_dir = "artifacts"
        os.makedirs(artifacts_dir, exist_ok=True)
        vec_path = os.path.join(artifacts_dir, "tfidf_vectorizer.pkl")
        model_path = os.path.join(artifacts_dir, "classifier.pkl")
        joblib.dump(vectorizer, vec_path)
        joblib.dump(model, model_path)

        mlflow.log_artifact(vec_path, artifact_path="preprocessing")
        mlflow.log_artifact(model_path, artifact_path="model")

        # Logar como modelo MLflow também
        mlflow.sklearn.log_model(model, artifact_path="sklearn-model")

        latency_ms = (time.time() - start_ts) * 1000.0

        return {
            "status": "completed",
            "run_id": run_id,
            "metrics": {
                "accuracy": acc,
                "log_loss": ll,
                "latency_ms": latency_ms,
                "info": f"Treino com MLflow no experimento '{experiment_name}'"
            }
        }
