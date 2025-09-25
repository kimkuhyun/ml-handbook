# streamlit_app/core/loaders.py
from __future__ import annotations
import pandas as pd
import joblib
from typing import List

def _infer_class_names(model) -> List[str]:
    if hasattr(model, "classes_"):
        classes = model.classes_
    elif hasattr(model, "named_steps"):
        last = list(model.named_steps.values())[-1]
        classes = getattr(last, "classes_", None)
    else:
        classes = None
    if classes is None:
        classes = list(range(21))
    return [str(c) for c in classes]

def load_probs_from_csv(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    id_col = "ID" if "ID" in df.columns else df.columns[0]
    cls_cols = [c for c in df.columns if c != id_col]
    std = {}
    for c in cls_cols:
        base = str(c).lower().lstrip("c")
        try:
            std[c] = str(int(base))
        except:
            std[c] = str(c)
    df = df.rename(columns=std)
    return df[[id_col] + [std[c] for c in cls_cols]]

def load_model_and_predict_probs(file, X: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(file)
    classes = _infer_class_names(model)
    proba = model.predict_proba(X.drop(columns=[c for c in ["ID"] if c in X.columns]).values)
    out = pd.DataFrame(proba, columns=[str(c) for c in classes])
    out.insert(0, "ID", X["ID"].values if "ID" in X.columns else range(len(X)))
    return out

def probs_to_counts(df_probs: pd.DataFrame) -> pd.DataFrame:
    id_col = "ID" if "ID" in df_probs.columns else df_probs.columns[0]
    cls_cols = [c for c in df_probs.columns if c != id_col]
    preds = df_probs[cls_cols].astype(float).idxmax(axis=1)
    counts = preds.value_counts().reindex(cls_cols, fill_value=0).reset_index()
    counts.columns = ["class", "count"]
    counts["class"] = counts["class"].astype(str)
    return counts

