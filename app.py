import streamlit as st
import numpy as np

# --- Full List of CMS Star Ratings Metric Config ---
# Source: CMS Medicare Advantage Star Ratings (simplified categories)
metrics = [
    # Staying Healthy
    {"name": "Breast Cancer Screening", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 69, 2), (70, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Colorectal Cancer Screening", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 69, 2), (70, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Annual Flu Vaccine", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 69, 2), (70, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Adult BMI Assessment", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 69, 2), (70, 79, 3), (80, 89, 4), (90, 100, 5)]},

    # Managing Chronic Conditions
    {"name": "Diabetes Care – Eye Exam", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 49, 1), (50, 64, 2), (65, 74, 3), (75, 89, 4), (90, 100, 5)]},
    {"name": "Diabetes Care – Kidney Disease Monitoring", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 49, 1), (50, 64, 2), (65, 74, 3), (75, 89, 4), (90, 100, 5)]},
    {"name": "Diabetes Care – Blood Sugar Controlled", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 49, 1), (50, 64, 2), (65, 74, 3), (75, 89, 4), (90, 100, 5)]},
    {"name": "Controlling Blood Pressure", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 49, 1), (50, 64, 2), (65, 74, 3), (75, 89, 4), (90, 100, 5)]},
    {"name": "Rheumatoid Arthritis Management", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 65, 2), (66, 75, 3), (76, 89, 4), (90, 100, 5)]},
    {"name": "Statin Therapy for Cardiovascular Disease", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 65, 2), (66, 75, 3), (76, 89, 4), (90, 100, 5)]},

    # Member Experience (CAHPS)
    {"name": "Getting Needed Care", "min": 0, "max": 100, "weight": 4, "star_ranges": [(0, 50, 1), (51, 65, 2), (66, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Getting Appointments and Care Quickly", "min": 0, "max": 100, "weight": 4, "star_ranges": [(0, 50, 1), (51, 65, 2), (66, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Customer Service", "min": 0, "max": 100, "weight": 4, "star_ranges": [(0, 49, 1), (50, 64, 2), (65, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Rating of Health Plan", "min": 0, "max": 100, "weight": 4, "star_ranges": [(0, 50, 1), (51, 65, 2), (66, 79, 3), (80, 89, 4), (90, 100, 5)]},
    {"name": "Care Coordination", "min": 0, "max": 100, "weight": 4, "star_ranges": [(0, 50, 1), (51, 65, 2), (66, 79, 3), (80, 89, 4), (90, 100, 5)]},

    # Complaints and Member Retention
    {"name": "Complaints About the Health Plan", "min": 0, "max": 100, "weight": 1.5, "star_ranges": [(0, 25, 5), (26, 40, 4), (41, 60, 3), (61, 80, 2), (81, 100, 1)]},
    {"name": "Members Choosing to Leave the Plan", "min": 0, "max": 100, "weight": 1.5, "star_ranges": [(0, 10, 5), (11, 20, 4), (21, 30, 3), (31, 40, 2), (41, 100, 1)]},
    {"name": "Timely Appeals Decisions", "min": 0, "max": 100, "weight": 1.5, "star_ranges": [(0, 50, 1), (51, 70, 2), (71, 80, 3), (81, 90, 4), (91, 100, 5)]},

    # Administrative/Service Measures
    {"name": "Call Center — Language & TTY Access", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 50, 1), (51, 70, 2), (71, 80, 3), (81, 90, 4), (91, 100, 5)]},
    {"name": "Enrollment Timeliness", "min": 0, "max": 100, "weight": 1.5, "star_ranges": [(0, 50, 1), (51, 70, 2), (71, 80, 3), (81, 90, 4), (91, 100, 5)]},
    {"name": "Medication Adherence – Diabetes", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 59, 1), (60, 74, 2), (75, 84, 3), (85, 89, 4), (90, 100, 5)]},
    {"name": "Medication Adherence – Hypertension", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 59, 1), (60, 74, 2), (75, 84, 3), (85, 89, 4), (90, 100, 5)]},
    {"name": "Medication Adherence – Cholesterol", "min": 0, "max": 100, "weight": 3, "star_ranges": [(0, 59, 1), (60, 74, 2), (75, 84, 3), (85, 89, 4), (90, 100, 5)]},
    {"name": "MTM Program Completion Rate", "min": 0, "max": 100, "weight": 1, "star_ranges": [(0, 30, 1), (31, 50, 2), (51, 70, 3), (71, 85, 4), (86, 100, 5)]}
]

# --- Utility functions ---
def get_star_score(value, ranges):
    for low, high, score in ranges:
        if low <= value <= high:
            return score
    return 1

def color_slider(value):
    if value < 50:
        return '🔴'
    elif value < 70:
        return '🟠'
    elif value < 85:
        return '🟡'
    else:
        return '🟢'

# --- App Layout ---
st.set_page_config(page_title="CMS Star Rating Simulator", layout="wide")
st.title("⭐ CMS Star Rating Simulator for Medicare Advantage Plans")

st.markdown("""
This interactive simulator allows you to model your plan's STAR rating performance across various CMS metrics.
Adjust the sliders below to input your current performance for each KPI/metric.
""")

metric_inputs = []
weighted_scores = []

st.subheader("📊 Metric Performance Inputs")

cols = st.columns(2)

for idx, metric in enumerate(metrics):
    with cols[idx % 2]:
        val = st.slider(
            label=f"{metric['name']} ({metric['weight']}x weight)",
            min_value=metric['min'],
            max_value=metric['max'],
            value=int((metric['max'] + metric['min']) / 2),
            step=1
        )
        star_score = get_star_score(val, metric['star_ranges'])
        st.write(f"Performance: {val} {color_slider(val)} → ⭐ {star_score}")
        metric_inputs.append({"name": metric['name'], "value": val, "star_score": star_score, "weight": metric['weight']})
        weighted_scores.append(star_score * metric['weight'])

# --- Overall STAR Rating Calculation ---
total_weight = sum(m['weight'] for m in metrics)
overall_star_rating = round(sum(weighted_scores) / total_weight, 2)

st.markdown("---")
st.header(f"📈 Overall Predicted STAR Rating: ⭐ {overall_star_rating}")

# --- AI Recommendations (Simple Rule-based) ---
st.subheader("🧠 AI Recommendations")
for m in metric_inputs:
    if m['star_score'] < 4:
        st.markdown(f"**{m['name']}**: Improve from ⭐ {m['star_score']} by enhancing provider outreach, member engagement, and closing care gaps.")

st.markdown("---")
st.caption("Data and weights based on CMS Medicare Advantage Star Ratings (2025 policy year, simplified for demonstration)")
