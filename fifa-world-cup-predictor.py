import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

team_data = {
    'Argentina': {'fifa_rank': 1, 'attack': 95, 'defense': 90, 'form': 9, 'star_player': 'Messi'},
    'Brazil': {'fifa_rank': 2, 'attack': 94, 'defense': 88, 'form': 8, 'star_player': 'Vinicius Jr'},
    'France': {'fifa_rank': 3, 'attack': 93, 'defense': 89, 'form': 8, 'star_player': 'Mbappé'},
    'England': {'fifa_rank': 4, 'attack': 90, 'defense': 85, 'form': 7, 'star_player': 'Bellingham'},
    'Spain': {'fifa_rank': 5, 'attack': 88, 'defense': 87, 'form': 7, 'star_player': 'Rodri'},
    'Germany': {'fifa_rank': 6, 'attack': 87, 'defense': 86, 'form': 7, 'star_player': 'Musiala'},
    'Portugal': {'fifa_rank': 7, 'attack': 89, 'defense': 84, 'form': 7, 'star_player': 'Ronaldo'},
    'Netherlands': {'fifa_rank': 8, 'attack': 86, 'defense': 85, 'form': 6, 'star_player': 'Van Dijk'},
    'Italy': {'fifa_rank': 9, 'attack': 84, 'defense': 88, 'form': 6, 'star_player': 'Donnarumma'},
    'Belgium': {'fifa_rank': 10, 'attack': 85, 'defense': 82, 'form': 6, 'star_player': 'De Bruyne'},
    'USA': {'fifa_rank': 11, 'attack': 82, 'defense': 80, 'form': 6, 'star_player': 'Pulisic'},
    'Mexico': {'fifa_rank': 12, 'attack': 80, 'defense': 78, 'form': 5, 'star_player': 'Lozano'},
    'Japan': {'fifa_rank': 13, 'attack': 79, 'defense': 81, 'form': 6, 'star_player': 'Mitoma'},
    'South Korea': {'fifa_rank': 14, 'attack': 78, 'defense': 79, 'form': 5, 'star_player': 'Son'},
    'Australia': {'fifa_rank': 15, 'attack': 76, 'defense': 77, 'form': 5, 'star_player': 'Goodwin'},
    'Nigeria': {'fifa_rank': 16, 'attack': 78, 'defense': 75, 'form': 5, 'star_player': 'Osimhen'},
    'Morocco': {'fifa_rank': 17, 'attack': 76, 'defense': 79, 'form': 6, 'star_player': 'Ashraf'},
}

knockout_teams = [
    'Argentina', 'Brazil', 'France', 'England', 'Spain', 'Germany',
    'Portugal', 'Netherlands', 'Italy', 'Belgium', 'USA', 'Mexico',
    'Japan', 'South Korea', 'Australia', 'Nigeria', 'Morocco'
]

def predict_match(team1, team2, venue="neutral"):
    """Predict match outcome based on team strengths"""
    
    t1 = team_data.get(team1, {'fifa_rank': 50, 'attack': 70, 'defense': 70, 'form': 5})
    t2 = team_data.get(team2, {'fifa_rank': 50, 'attack': 70, 'defense': 70, 'form': 5})
    
    t1_score = (t1['attack'] * 0.4 + t1['defense'] * 0.3 + t1['form'] * 10 + (101 - t1['fifa_rank']) * 0.5)
    t2_score = (t2['attack'] * 0.4 + t2['defense'] * 0.3 + t2['form'] * 10 + (101 - t2['fifa_rank']) * 0.5)
    
    if venue == "home":
        t1_score *= 1.05
    elif venue == "away":
        t2_score *= 1.05
    
    total = t1_score + t2_score
    t1_win_prob = (t1_score / total) * 100
    t2_win_prob = (t2_score / total) * 100
    
    diff = abs(t1_score - t2_score)
    draw_prob = max(0, 25 - diff * 0.3)
    
    if draw_prob > 0:
        t1_win_prob = t1_win_prob * (1 - draw_prob / 100)
        t2_win_prob = t2_win_prob * (1 - draw_prob / 100)
    
    return {
        'team1_win': t1_win_prob,
        'team2_win': t2_win_prob,
        'draw': draw_prob,
        'team1_score': t1_score,
        'team2_score': t2_score,
        'predicted_winner': team1 if t1_win_prob > t2_win_prob else team2
    }

quarterfinals = [
    ('Brazil', 'Argentina'),
    ('France', 'England'),
    ('Spain', 'Germany'),
    ('Portugal', 'Netherlands')
]

semifinals = [
    ('Winner QF1', 'Winner QF2'),
    ('Winner QF3', 'Winner QF4')
]

final = [
    ('Winner SF1', 'Winner SF2')
]

st.set_page_config(
    page_title="⚽ FIFA World Cup Predictor 2026",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2026 Predictor")
st.markdown("*Predict match outcomes based on FIFA rankings, team strength, and form*")

with st.sidebar:
    st.header("🔧 Settings")
    st.markdown("---")
    st.subheader("📊 Team Data")
    st.info(f"✅ {len(team_data)} teams loaded")
    st.markdown("---")
    st.caption("⚽ Powered by FIFA Rankings & Statistical Models")


tab1, tab2, tab3 = st.tabs(["🔮 Match Predictor", "🏆 Tournament Bracket", "📊 Team Stats"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("⚽ Select Match")
        
        team_options = list(team_data.keys())
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            team1 = st.selectbox("🏠 Team 1", team_options, index=0)
        
        with col_b:
            team2 = st.selectbox("✈️ Team 2", team_options, index=1)
        
        venue = st.selectbox("📍 Venue", ["neutral", "home", "away"])
        
        if st.button("🔮 Predict Match", type="primary", use_container_width=True):
            result = predict_match(team1, team2, venue)
            
            st.markdown("---")
            st.subheader("📊 Prediction Results")
            
            col_w1, col_w2, col_w3 = st.columns(3)
            with col_w1:
                st.metric(
                    label=f"🏠 {team1} Win",
                    value=f"{result['team1_win']:.1f}%",
                    delta=""
                )
            with col_w2:
                st.metric(
                    label="🤝 Draw",
                    value=f"{result['draw']:.1f}%",
                    delta=""
                )
            with col_w3:
                st.metric(
                    label=f"✈️ {team2} Win",
                    value=f"{result['team2_win']:.1f}%",
                    delta=""
                )
            
            st.markdown("---")
            st.subheader("📈 Probability Visualization")
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.progress(result['team1_win'] / 100)
                st.caption(f"{team1}: {result['team1_win']:.1f}%")
            with col_p2:
                st.progress(result['team2_win'] / 100)
                st.caption(f"{team2}: {result['team2_win']:.1f}%")
            
            st.markdown("---")
            if result['draw'] > 25:
                st.info("🤝 Match predicted to be a close draw!")
            else:
                winner = result['predicted_winner']
                st.success(f"🏆 Predicted Winner: **{winner}**")
            
            st.markdown("---")
            st.caption(f"⭐ {team1} Star: {team_data[team1]['star_player']} | ⭐ {team2} Star: {team_data[team2]['star_player']}")
    
    with col2:
        st.subheader("📊 Team Comparison")
        
        if team1 in team_data and team2 in team_data:
            t1 = team_data[team1]
            t2 = team_data[team2]
            
            comp_data = pd.DataFrame({
                'Attribute': ['FIFA Rank', 'Attack', 'Defense', 'Form'],
                team1: [t1['fifa_rank'], t1['attack'], t1['defense'], t1['form']],
                team2: [t2['fifa_rank'], t2['attack'], t2['defense'], t2['form']]
            })
            
            st.dataframe(comp_data, hide_index=True, use_container_width=True)
            
            # Radar chart
            categories = ['Attack', 'Defense', 'Form']
            values1 = [t1['attack'], t1['defense'], t1['form'] * 10]
            values2 = [t2['attack'], t2['defense'], t2['form'] * 10]
            
            fig, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(polar=True))
            
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            values1 += values1[:1]
            values2 += values2[:1]
            angles += angles[:1]
            
            ax.plot(angles, values1, 'o-', linewidth=2, label=team1, color='blue')
            ax.fill(angles, values1, alpha=0.25, color='blue')
            ax.plot(angles, values2, 'o-', linewidth=2, label=team2, color='red')
            ax.fill(angles, values2, alpha=0.25, color='red')
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 100)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            
            st.pyplot(fig)

with tab2:
    st.subheader("🏆 FIFA World Cup 2026 Knockout Stage")
    
    st.markdown("### Quarterfinals")
    for i, (t1, t2) in enumerate(quarterfinals, 1):
        col_a, col_b, col_c = st.columns([2, 1, 2])
        with col_a:
            st.write(f"**{t1}**")
        with col_b:
            st.write("vs")
        with col_c:
            st.write(f"**{t2}**")
    
    st.markdown("---")
    st.markdown("### Semifinals")
    for i, (t1, t2) in enumerate(semifinals, 1):
        col_a, col_b, col_c = st.columns([2, 1, 2])
        with col_a:
            st.write(f"**{t1}**")
        with col_b:
            st.write("vs")
        with col_c:
            st.write(f"**{t2}**")
    
    st.markdown("---")
    st.markdown("### Final")
    for i, (t1, t2) in enumerate(final, 1):
        col_a, col_b, col_c = st.columns([2, 1, 2])
        with col_a:
            st.write(f"**{t1}**")
        with col_b:
            st.write("vs")
        with col_c:
            st.write(f"**{t2}**")
    
    st.warning("🏆 Click 'Predict Match' in the Match Predictor tab to see predictions!")

with tab3:
    st.subheader("📊 Team Statistics")
    
    # Convert to DataFrame
    stats_data = []
    for team, data in team_data.items():
        stats_data.append({
            'Team': team,
            'FIFA Rank': data['fifa_rank'],
            'Attack': data['attack'],
            'Defense': data['defense'],
            'Form': data['form'],
            'Star Player': data['star_player']
        })
    
    df = pd.DataFrame(stats_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("---")
st.caption("⚽ FIFA World Cup 2026 Predictor | Built with Streamlit")