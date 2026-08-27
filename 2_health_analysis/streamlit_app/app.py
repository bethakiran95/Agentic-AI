import warnings

from dotenv import load_dotenv
import streamlit as st

from analysis import extract_blood_values, generate_diet_plan, split_response
from llm_client import get_llm

warnings.filterwarnings(
    "ignore",
    message="Direct use of automatic function calling",
)

load_dotenv()

st.set_page_config(page_title="Blood Work Analyzer", layout="wide")

llm = get_llm()

st.markdown("""
<style>
.scroll-box {
    height: 230px;
    overflow-y: auto;
    padding: 12px 16px;
    border: 1px solid #333;
    border-radius: 8px;
    background-color: #1e1e1e;
    font-size: 0.9rem;
    line-height: 1.6;
}
.scroll-box p, .scroll-box li {
    color: #e0e0e0;
}
.section-label {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 6px;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.title("Blood Work Analyzer")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Blood Work Report")
    blood_report = st.text_area(
        label="Paste your report below",
        height=500,
        placeholder="Paste your blood work report here...",
        label_visibility="collapsed"
    )
    analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

with right_col:
    st.subheader("Health Summary")
    health_box = st.empty()
    health_box.markdown('<div class="scroll-box"></div>', unsafe_allow_html=True)

    st.subheader("Suggested Diet Plan")
    diet_box = st.empty()
    diet_box.markdown('<div class="scroll-box"></div>', unsafe_allow_html=True)

if analyze_clicked:
    if not blood_report.strip():
        with left_col:
            st.warning("Please paste a blood work report before analyzing.")
    else:
        with st.spinner("Analyzing your blood work..."):
            extracted_values = extract_blood_values(llm, blood_report)
            full_response = generate_diet_plan(llm, extracted_values)

        health_summary, diet_plan = split_response(full_response)

        # Render into fixed-height scrollable boxes
        health_box.markdown(
            f'<div class="scroll-box">{health_summary}</div>',
            unsafe_allow_html=True
        )
        diet_box.markdown(
            f'<div class="scroll-box">{diet_plan if diet_plan else full_response}</div>',
            unsafe_allow_html=True
        )
