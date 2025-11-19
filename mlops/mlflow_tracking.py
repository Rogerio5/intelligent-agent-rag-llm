import os
import mlflow

def log_inference(inputs: dict, outputs: dict, metadata: dict = None):
    try:
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT", "agente-inteligente"))
        with mlflow.start_run(run_name="inference", nested=True):
            mlflow.log_dict(inputs, "inputs.json")
            mlflow.log_dict(outputs, "outputs.json")
            if metadata:
                for k, v in metadata.items():
                    if isinstance(v, (int, float)):
                        mlflow.log_metric(k, float(v))
                    else:
                        mlflow.log_param(k, str(v))
    except Exception:
        # não falhar produção por causa de tracking
        pass
