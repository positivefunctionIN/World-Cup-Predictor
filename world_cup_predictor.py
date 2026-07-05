import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def predict_win(target, current_score, wickets_down, overs_done):
    if target <= 0 or current_score <= 0 or overs_done <= 0:
        return 50
    
    overs_remaining = max(20 - overs_done, 0.1)
    required_run_rate = (target - current_score) / overs_remaining
    current_run_rate = current_score / overs_done if overs_done > 0 else 0
    
    wicket_penalty = wickets_down * 5
    base_prob = 50
    
    if current_run_rate > required_run_rate * 1.3:
        base_prob = 85
    elif current_run_rate > required_run_rate * 1.1:
        base_prob = 70
    elif current_run_rate > required_run_rate * 0.9:
        base_prob = 50
    elif current_run_rate > required_run_rate * 0.7:
        base_prob = 30
    else:
        base_prob = 15
    
    final_prob = max(base_prob - wicket_penalty, 5)
    return min(final_prob, 95)  

st.set_page_config(
    page_title="🏏 World Cup Predictor",
    page_icon="🏏",
    layout="centered"
)

st.title("🏏 World Cup 2026 Match Predictor")
st.markdown("*Predict the winning probability of the batting team*")

col1, col2 = st.columns(2)

with col1:
    target = st.number_input("Target Score", min_value=50, max_value=400, value=180, step=10)
    current_score = st.number_input("Current Score", min_value=0, max_value=400, value=120, step=5)
    
with col2:
    wickets_down = st.slider("Wickets Lost", min_value=0, max_value=10, value=5)
    overs_done = st.slider("Overs Bowled", min_value=0.0, max_value=20.0, value=15.0, step=0.1)

win_prob = predict_win(target, current_score, wickets_down, overs_done)

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.metric(
        label="🏆 Win Probability",
        value=f"{win_prob:.1f}%",
        delta=f"{win_prob - 50:.1f}% vs 50/50"
    )

st.progress(win_prob / 100)

fig, ax = plt.subplots(figsize=(6, 1))
ax.barh([0], [win_prob], color='green' if win_prob > 50 else 'red', height=0.3)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xlabel("Win Probability (%)")
ax.set_title("Probability Gauge")
ax.axvline(x=50, color='black', linestyle='--', alpha=0.5)
st.pyplot(fig)

st.markdown("---")
st.subheader("📊 Match Context")
st.write(f"**Target:** {target} runs")
st.write(f"**Current Score:** {current_score}/{wickets_down} in {overs_done:.1f} overs")
st.write(f"**Required Run Rate:** {(target - current_score) / max(20 - overs_done, 0.1):.2f} runs/over")
st.write(f"**Current Run Rate:** {current_score / overs_done if overs_done > 0 else 0:.2f} runs/over")

st.markdown("---")
st.caption("🏏 Built for FIFA World Cup 2026 | Predicts win probability based on match context")