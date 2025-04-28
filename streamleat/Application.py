import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(
    page_title="Gilet Connecté - Tableau de bord",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonctions pour générer des données simulées
def generate_heart_rate_data(duration_hours=12, interval_minutes=5):
    """Génère des données de fréquence cardiaque simulées"""
    now = datetime.now()
    start_time = now - timedelta(hours=duration_hours)
    
    # Créer une liste de timestamps
    timestamps = []
    current = start_time
    while current <= now:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)
    
    # Générer des valeurs de fréquence cardiaque simulées
    base_hr = 70  # BPM moyen au repos
    heart_rates = []
    
    for i in range(len(timestamps)):
        time_of_day = timestamps[i].hour
        
        # Simuler des variations selon l'heure de la journée
        if 6 <= time_of_day < 9:  # Matin (activité)
            hr = base_hr + 20 + random.uniform(-5, 15)
        elif 12 <= time_of_day < 14:  # Midi (après repas)
            hr = base_hr + 10 + random.uniform(-3, 10)
        elif 17 <= time_of_day < 20:  # Soir (exercice)
            hr = base_hr + 30 + random.uniform(-5, 20)
        else:  # Reste de la journée
            hr = base_hr + random.uniform(-8, 8)
        
        heart_rates.append(round(hr))
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'heart_rate': heart_rates
    })

def generate_temperature_data(duration_hours=12, interval_minutes=5):
    """Génère des données de température corporelle simulées"""
    now = datetime.now()
    start_time = now - timedelta(hours=duration_hours)
    
    timestamps = []
    current = start_time
    while current <= now:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)
    
    # Température corporelle de base
    base_temp = 36.5
    temperatures = []
    
    for i in range(len(timestamps)):
        time_of_day = timestamps[i].hour
        
        # Variations diurnes normales de la température corporelle
        if 0 <= time_of_day < 6:  # Nuit (plus basse)
            temp = base_temp - 0.3 + random.uniform(-0.2, 0.1)
        elif 12 <= time_of_day < 18:  # Après-midi (plus haute)
            temp = base_temp + 0.2 + random.uniform(-0.1, 0.3)
        else:
            temp = base_temp + random.uniform(-0.2, 0.2)
        
        temperatures.append(round(temp, 1))
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'temperature': temperatures
    })

def generate_activity_data(duration_hours=12, interval_minutes=5):
    """Génère des données d'activité simulées (pas, mouvements)"""
    now = datetime.now()
    start_time = now - timedelta(hours=duration_hours)
    
    timestamps = []
    current = start_time
    while current <= now:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)
    
    steps = []
    movements = []
    cumulative_steps = 0
    
    for i in range(len(timestamps)):
        time_of_day = timestamps[i].hour
        
        # Simuler différentes périodes d'activité
        if 7 <= time_of_day < 9:  # Matin actif
            new_steps = random.randint(300, 800)
            movement = random.uniform(7, 10)
        elif 12 <= time_of_day < 14:  # Déjeuner/marche
            new_steps = random.randint(200, 500)
            movement = random.uniform(4, 7)
        elif 17 <= time_of_day < 19:  # Sport/exercice du soir
            new_steps = random.randint(1000, 2000)
            movement = random.uniform(8, 10)
        elif 22 <= time_of_day or time_of_day < 6:  # Nuit/sommeil
            new_steps = random.randint(0, 20)
            movement = random.uniform(0, 2)
        else:  # Activité normale pendant la journée
            new_steps = random.randint(50, 300)
            movement = random.uniform(3, 6)
        
        cumulative_steps += new_steps
        steps.append(cumulative_steps)
        movements.append(round(movement, 1))
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'steps': steps,
        'movement_intensity': movements
    })

def generate_posture_data(duration_hours=12, interval_minutes=5):
    """Génère des données de posture simulées"""
    now = datetime.now()
    start_time = now - timedelta(hours=duration_hours)
    
    timestamps = []
    current = start_time
    while current <= now:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)
    
    postures = []
    
    for i in range(len(timestamps)):
        time_of_day = timestamps[i].hour
        
        # Simuler différentes postures selon l'heure
        if 0 <= time_of_day < 7:  # Sommeil
            posture = "allongé"
        elif 8 <= time_of_day < 12 or 14 <= time_of_day < 18:  # Travail
            if random.random() < 0.8:
                posture = "assis"
            else:
                posture = "debout"
        elif 12 <= time_of_day < 14:  # Déjeuner
            if random.random() < 0.6:
                posture = "assis"
            else:
                posture = "debout"
        else:  # Soirée
            if random.random() < 0.5:
                posture = "assis"
            elif random.random() < 0.8:
                posture = "debout"
            else:
                posture = "allongé"
        
        postures.append(posture)
    
    # Simuler quelques mauvaises postures
    for i in range(len(postures)):
        if postures[i] == "assis" and random.random() < 0.2:
            postures[i] = "mauvaise posture"
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'posture': postures
    })

def generate_alerts(hr_data, temp_data, posture_data):
    """Génère des alertes basées sur les données"""
    alerts = []
    
    # Alerte rythme cardiaque élevé
    high_hr = hr_data[hr_data['heart_rate'] > 100]
    for _, row in high_hr.iterrows():
        alerts.append({
            'timestamp': row['timestamp'],
            'type': 'Rythme cardiaque élevé',
            'value': f"{row['heart_rate']} BPM",
            'severity': 'warning'
        })
    
    # Alerte température élevée
    high_temp = temp_data[temp_data['temperature'] > 37.5]
    for _, row in high_temp.iterrows():
        alerts.append({
            'timestamp': row['timestamp'],
            'type': 'Température élevée',
            'value': f"{row['temperature']}°C",
            'severity': 'danger'
        })
    
    # Alerte mauvaise posture
    bad_posture = posture_data[posture_data['posture'] == 'mauvaise posture']
    for _, row in bad_posture.iterrows():
        alerts.append({
            'timestamp': row['timestamp'],
            'type': 'Mauvaise posture détectée',
            'value': "Correction recommandée",
            'severity': 'info'
        })
    
    # Simuler une détection de chute
    if random.random() < 0.3:  # 30% de chance d'avoir une chute
        fall_time = datetime.now() - timedelta(hours=random.randint(1, 8))
        alerts.append({
            'timestamp': fall_time,
            'type': 'Chute détectée',
            'value': "Intervention recommandée",
            'severity': 'danger'
        })
    
    return pd.DataFrame(alerts).sort_values('timestamp', ascending=False)

# Interface utilisateur
def main():
    # Barre latérale
    st.sidebar.image("aa.png", width=150)
    st.sidebar.title("Gilet Connecté")
    
    # Options utilisateur
    user_name = st.sidebar.text_input("Nom de l'utilisateur", "Jean Dupont")
    st.sidebar.subheader("État du gilet")
    
    # Statut du gilet
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Batterie", "78%")
    with col2:
        st.metric("Signal", "Bon")
    
    # Menu de navigation
    page = st.sidebar.radio("Navigation", ["Tableau de bord", "Historique", "Paramètres"])
    
    # Générer les données simulées
    heart_rate_data = generate_heart_rate_data()
    temperature_data = generate_temperature_data()
    activity_data = generate_activity_data()
    posture_data = generate_posture_data()
    alerts = generate_alerts(heart_rate_data, temperature_data, posture_data)
    
    # Page Tableau de bord
    if page == "Tableau de bord":
        st.title(f"Tableau de bord de {user_name}")
        
        # Métriques en direct
        st.subheader("Données en temps réel")
        col1, col2, col3, col4 = st.columns(4)
        
       
        with col1:
            current_hr = heart_rate_data['heart_rate'].iloc[-1]
            delta_hr = int(current_hr - heart_rate_data['heart_rate'].iloc[-2])  # Conversion en int standard
            st.metric("Rythme cardiaque", f"{current_hr} BPM", delta=delta_hr)

        with col2:
            current_temp = temperature_data['temperature'].iloc[-1]
            delta_temp = float(round(current_temp - temperature_data['temperature'].iloc[-2], 1))  # Conversion en float standard
            st.metric("Température", f"{current_temp}°C", delta=delta_temp)

        with col3:
            current_steps = activity_data['steps'].iloc[-1]
            delta_steps = int(activity_data['steps'].iloc[-1] - activity_data['steps'].iloc[-2])  # Conversion en int standard
            st.metric("Pas aujourd'hui", f"{current_steps}", delta=delta_steps)

        with col4:
            current_posture = posture_data['posture'].iloc[-1]
            st.metric("Posture actuelle", current_posture)
        
        # Graphiques
        st.subheader("Évolution récente")
        
        # Onglets pour différents graphiques
        tab1, tab2, tab3 = st.tabs(["Rythme cardiaque", "Température", "Activité"])
        
        with tab1:
            # Graphique de rythme cardiaque
            fig_hr = px.line(heart_rate_data, x='timestamp', y='heart_rate', 
                           title="Évolution du rythme cardiaque",
                           labels={"timestamp": "Heure", "heart_rate": "BPM"})
            fig_hr.update_layout(height=400)
            st.plotly_chart(fig_hr, use_container_width=True)
        
        with tab2:
            # Graphique de température
            fig_temp = px.line(temperature_data, x='timestamp', y='temperature',
                             title="Évolution de la température corporelle",
                             labels={"timestamp": "Heure", "temperature": "°C"})
            fig_temp.update_layout(height=400)
            fig_temp.update_traces(line_color='firebrick')
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with tab3:
            # Graphique d'activité
            fig_activity = go.Figure()
            
            # Ajouter les pas (axe y gauche)
            fig_activity.add_trace(go.Scatter(
                x=activity_data['timestamp'],
                y=activity_data['steps'],
                name='Pas cumulés',
                line=dict(color='royalblue')
            ))
            
            # Ajouter l'intensité des mouvements (axe y droit)
            fig_activity.add_trace(go.Scatter(
                x=activity_data['timestamp'],
                y=activity_data['movement_intensity'],
                name='Intensité de mouvement',
                line=dict(color='orange'),
                yaxis='y2'
            ))
            
            # Mise en page avec deux axes y
            fig_activity.update_layout(
                title="Activité physique",
                xaxis=dict(title="Heure"),
                yaxis=dict(title="Pas cumulés", side='left'),
                yaxis2=dict(title="Intensité", side='right', overlaying='y'),
                height=400,
                legend=dict(x=0.01, y=0.99)
            )
            
            st.plotly_chart(fig_activity, use_container_width=True)
        
        # Alertes
        st.subheader("Alertes récentes")
        if len(alerts) > 0:
            for _, alert in alerts.head(5).iterrows():
                severity_color = "blue"
                if alert['severity'] == 'warning':
                    severity_color = "orange"
                elif alert['severity'] == 'danger':
                    severity_color = "red"
                
                st.markdown(f"""
                <div style="border-left: 4px solid {severity_color}; padding-left: 10px; margin-bottom: 10px;">
                    <b>{alert['type']}</b> - {alert['value']}<br>
                    <small>{alert['timestamp'].strftime('%d/%m/%Y %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucune alerte récente")
    
    # Page Historique
    elif page == "Historique":
        st.title("Historique des données")
        
        # Sélection de la période
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Date de début", datetime.now().date() - timedelta(days=7))
        with col2:
            end_date = st.date_input("Date de fin", datetime.now().date())
        
        # Sélection des données à afficher
        data_type = st.multiselect("Données à afficher", 
                                  ["Rythme cardiaque", "Température", "Activité", "Posture"],
                                  default=["Rythme cardiaque"])
        
        # Affichage d'un message de démonstration
        st.info("Ceci est une démonstration. Dans une vraie application, des données historiques seraient chargées selon vos sélections.")
        
        # Affichage des graphiques selon la sélection
        if "Rythme cardiaque" in data_type:
            st.subheader("Historique du rythme cardiaque")
            # Simulations de données sur 7 jours
            dates = [datetime.now().date() - timedelta(days=x) for x in range(7)]
            avg_hr = [random.randint(65, 80) for _ in range(7)]
            max_hr = [x + random.randint(15, 40) for x in avg_hr]
            min_hr = [x - random.randint(5, 15) for x in avg_hr]
            
            hr_history = pd.DataFrame({
                'date': dates,
                'min_hr': min_hr,
                'avg_hr': avg_hr,
                'max_hr': max_hr
            })
            
            fig_hr_history = go.Figure()
            fig_hr_history.add_trace(go.Scatter(
                x=hr_history['date'], y=hr_history['max_hr'],
                name='Maximum', line=dict(color='red')
            ))
            fig_hr_history.add_trace(go.Scatter(
                x=hr_history['date'], y=hr_history['avg_hr'],
                name='Moyenne', line=dict(color='blue')
            ))
            fig_hr_history.add_trace(go.Scatter(
                x=hr_history['date'], y=hr_history['min_hr'],
                name='Minimum', line=dict(color='green')
            ))
            
            fig_hr_history.update_layout(height=400)
            st.plotly_chart(fig_hr_history, use_container_width=True)
        
        if "Activité" in data_type:
            st.subheader("Historique d'activité")
            
            # Simuler des données hebdomadaires de pas
            dates = [datetime.now().date() - timedelta(days=x) for x in range(7)]
            daily_steps = [random.randint(3000, 12000) for _ in range(7)]
            
            steps_history = pd.DataFrame({
                'date': dates,
                'steps': daily_steps
            })
            
            fig_steps = px.bar(steps_history, x='date', y='steps',
                             title="Pas quotidiens",
                             labels={"date": "Date", "steps": "Nombre de pas"})
            fig_steps.update_layout(height=400)
            st.plotly_chart(fig_steps, use_container_width=True)
    
    # Page Paramètres
    elif page == "Paramètres":
        st.title("Paramètres du gilet connecté")
        
        st.subheader("Profil utilisateur")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nom", "Jean")
            st.text_input("Prénom", "Dupont")
            st.date_input("Date de naissance", datetime(1980, 1, 1))
        with col2:
            st.number_input("Poids (kg)", min_value=30, max_value=200, value=75)
            st.number_input("Taille (cm)", min_value=100, max_value=250, value=175)
            st.selectbox("Sexe", ["Homme", "Femme", "Autre"])
        
        st.subheader("Paramètres des capteurs")
        
        # Paramètres des seuils d'alerte
        st.slider("Seuil d'alerte - Rythme cardiaque (BPM)", 80, 200, 120)
        st.slider("Seuil d'alerte - Température (°C)", 36.0, 40.0, 38.0, 0.1)
        
        # Options de notification
        st.subheader("Notifications")
        st.checkbox("Alertes de chute", value=True)
        st.checkbox("Alertes de rythme cardiaque", value=True)
        st.checkbox("Alertes de température", value=True)
        st.checkbox("Rappels de posture", value=True)
        
        # Fréquence d'échantillonnage
        st.subheader("Fréquence d'échantillonnage")
        st.select_slider("Fréquence de mesure", 
                       options=["1 minute", "5 minutes", "15 minutes", "30 minutes", "1 heure"],
                       value="5 minutes")
        
        # Contact d'urgence
        st.subheader("Contact d'urgence")
        st.text_input("Nom du contact", "Marie Dupont")
        st.text_input("Téléphone", "+33 6 12 34 56 78")
        
        # Bouton de sauvegarde
        if st.button("Sauvegarder les paramètres"):
            st.success("Paramètres sauvegardés avec succès!")

if __name__ == "__main__":
    main()