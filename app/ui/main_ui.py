import streamlit as st

# Page configuration
st.set_page_config(page_title="SENTRA", layout="wide")

# Header
st.title("SENTRA")
st.subheader("AI Policy Governance & Decision Intelligence Platform")

st.markdown("---")

# Decision input
st.text_area(
    "Describe the workplace decision you want to evaluate:",
    height=150,
    placeholder="Example: Can an intern work remotely using a personal laptop?"
)

st.button("Evaluate Decision")

st.markdown("## Evaluation Result (Preview)")

# Output placeholders
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk Level", "—")

with col2:
    st.metric("Policy Evidence", "—")

with col3:
    st.metric("Recommendation", "—")

st.markdown("### Reasoning")
st.write("Explanation will appear here.")

st.markdown("### Safer Alternative")
st.write("Suggested alternatives will appear here.")
