import streamlit as st
import time
import os
import tempfile

st.set_page_config(
    page_title="AI Mock Interview Assistant",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

from modules.semantic_analysis import analyze_semantic_similarity
from modules.sentiment_analysis import analyze_sentiment
from modules.filler_detection import detect_filler_words
from modules.grammar_analysis import analyze_grammar
from modules.confidence_score import calculate_confidence_score
from modules.feedback_generator import generate_feedback

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Caveat:wght@500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background-color: #fdf6ee;
}

[data-testid="stSidebar"] {
    background-color: #fff8f0;
    border-right: 2px dashed #f0d9c0;
}

.stButton > button {
    background: #fff;
    color: #4a3728;
    border: 2px solid #e8cdb0;
    border-radius: 10px;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 8px 16px;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #fff3e6;
    border-color: #d4956a;
    color: #d4956a;
}

.stTextArea textarea {
    background: #fff !important;
    border: 2px solid #e8cdb0 !important;
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    color: #3d2e22 !important;
}

.stTextArea textarea:focus {
    border-color: #d4956a !important;
    box-shadow: 0 0 0 3px rgba(212,149,106,0.15) !important;
}

.stSelectbox > div > div {
    background: #fff !important;
    border: 2px solid #e8cdb0 !important;
    border-radius: 10px !important;
    color: #3d2e22 !important;
    font-family: 'Nunito', sans-serif !important;
}

.stRadio label {
    color: #4a3728 !important;
    font-weight: 600;
}

.page-title {
    font-family: 'Caveat', cursive;
    font-size: 2rem;
    color: #3d2e22;
    font-weight: 600;
    margin-bottom: 2px;
}

.subtitle {
    font-size: 0.9rem;
    color: #9c7b5e;
    margin-bottom: 24px;
}

.section-label {
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #c47a3a;
    margin-bottom: 10px;
    margin-top: 24px;
}

.q-card {
    background: #fff;
    border: 2px solid #e8cdb0;
    border-left: 5px solid #d4956a;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 20px;
}

.q-card .q-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #3d2e22;
    line-height: 1.5;
}

.q-card .q-tip {
    font-size: 0.82rem;
    color: #a07850;
    margin-top: 8px;
}

.q-tag {
    display: inline-block;
    background: #fff3e6;
    color: #c47a3a;
    border: 1px solid #f0d0a8;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 2px 10px;
    margin-bottom: 8px;
}

.score-pill {
    background: #fff;
    border: 2px solid #e8cdb0;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
}

.score-num {
    font-family: 'Caveat', cursive;
    font-size: 2.4rem;
    font-weight: 600;
    line-height: 1.1;
}

.score-lbl {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #9c7b5e;
    margin-top: 2px;
}

.fb-item {
    background: #fff;
    border: 1.5px solid #e8cdb0;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 9px;
    font-size: 0.9rem;
    color: #3d2e22;
    line-height: 1.5;
}

.fb-positive {
    border-left: 4px solid #5cb85c;
}

.fb-warning {
    border-left: 4px solid #e8a020;
}

.fb-info {
    border-left: 4px solid #5b9bd5;
}

.transcript {
    background: #fff;
    border: 2px dashed #e8cdb0;
    border-radius: 10px;
    padding: 16px;
    font-size: 0.9rem;
    color: #5a3e2b;
    line-height: 1.7;
    min-height: 80px;
}

.err-item {
    background: #fffbf0;
    border: 1.5px solid #f0d0a8;
    border-left: 4px solid #e8a020;
    border-radius: 8px;
    padding: 9px 14px;
    margin-bottom: 7px;
    font-size: 0.83rem;
    color: #5a3e2b;
}

.filler-badge {
    display: inline-block;
    background: #fff3e6;
    border: 1.5px solid #f0c080;
    color: #c47a3a;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 9px;
    margin: 3px 3px 3px 0;
}

.rec-box {
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    margin-top: 20px;
    border: 2px solid;
}

.rec-great {
    background: #f0fff4;
    border-color: #5cb85c;
}

.rec-good {
    background: #f0fff4;
    border-color: #84cc16;
}

.rec-ok {
    background: #fffbf0;
    border-color: #e8a020;
}

.rec-low {
    background: #fff5f5;
    border-color: #e05c5c;
}

.feat-card {
    background: #fff;
    border: 2px solid #e8cdb0;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
}

.feat-icon {
    font-size: 1.7rem;
    margin-bottom: 8px;
}

.feat-title {
    font-size: 1rem;
    font-weight: 800;
    color: #3d2e22;
    margin-bottom: 4px;
}

.feat-desc {
    font-size: 0.83rem;
    color: #9c7b5e;
    line-height: 1.5;
}

.hist-item {
    background: #fff;
    border: 2px solid #e8cdb0;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}

[data-testid="metric-container"] {
    background: #fff;
    border: 2px solid #e8cdb0;
    border-radius: 10px;
    padding: 12px;
}

h1,h2,h3,h4 {
    color: #3d2e22 !important;
}

p, li {
    color: #5a3e2b;
}

label {
    color: #4a3728 !important;
}

hr {
    border-color: #e8cdb0;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)