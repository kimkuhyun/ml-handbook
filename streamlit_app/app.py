# streamlit_app/app.py
from __future__ import annotations

from pathlib import Path
import sys
import streamlit as st

# 프로젝트 루트 경로 주입
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from streamlit_app.core.base import App
# ↓ 레지스트리에 등록시키기 위해 임포트 (파일명만 변경)
import streamlit_app.views.home      # noqa: F401
import streamlit_app.views.mlp       # noqa: F401
import streamlit_app.views.lightgbm  # noqa: F401
import streamlit_app.views.blending  # noqa: F401
import streamlit_app.views.lda_svm   # noqa: F401
import streamlit_app.views.logreg       # noqa: F401
import streamlit_app.views.random_forest  # noqa: F401
import streamlit_app.views.svm          # noqa: F401
import streamlit_app.views.qda          # noqa: F401
import streamlit_app.views.knn          # noqa: F401
import streamlit_app.views.catboost     # noqa: F401
import streamlit_app.views.cascade      # noqa: F401
import streamlit_app.views.xgboost      # noqa: F401
import streamlit_app.views.eda                    # noqa: F401
# --- Preprocessing new pages ---
import streamlit_app.views.preprocess_standardize # noqa: F401
import streamlit_app.views.preprocess_feature_selection_top30  # noqa: F401
import streamlit_app.views.preprocess_corr_pruning            # noqa: F401
import streamlit_app.views.preprocess_lda_features            # noqa: F401
import streamlit_app.views.preprocess_autoencoder_latent      # noqa: F401
import streamlit_app.views.preprocess_outlier_policy          # noqa: F401
import streamlit_app.views.preprocess_experiments  # noqa: F401
import streamlit_app.views.preprocess_iqr          # noqa: F401

# --- Regularization new pages ---
import streamlit_app.views.regularization_overview# noqa: F401
import streamlit_app.views.regularization_weightdecay_earlystop  # noqa: F401
import streamlit_app.views.regularization_batchnorm_noise        # noqa: F401
import streamlit_app.views.regularization_calibration            # noqa: F401
import streamlit_app.views.regularization_bagging                # noqa: F401
import streamlit_app.views.regularization_gating

import streamlit_app.views.results_overview      # noqa: F401
import streamlit_app.views.results_stage         # noqa: F401
import streamlit_app.views.results_postprocess   # noqa: F401
import streamlit_app.views.results_stacking_variants  # noqa: F401
import streamlit_app.views.results_learning_curves    # noqa: F401

import streamlit_app.views.predict_dist

st.set_page_config(page_title="우리만의 AI 교과서 · Home", page_icon="📘", layout="wide")

def main():
    app = App(project_title="우리만의 AI 교과서", repo_name="ml-handbook")
    app.run()

if __name__ == "__main__":
    main()

