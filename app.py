import streamlit as st
import pandas as pd
import plotly.express as px
from src.nlp_processing import match_column, detect_groupby

# PAGE CONFIG
st.set_page_config(
    page_title="AI BI Chatbot",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.chat-user {
    background-color: #2563eb;
    padding: 12px;
    border-radius: 10px;
    color: white;
    margin-bottom: 10px;
}

.chat-bot {
    background-color: #e5e7eb;
    color: #111827;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.title("AI Business Intelligence Chatbot")
st.caption("Ask questions about your dataset in natural language")

st.markdown("---")

# SIDEBAR
with st.sidebar:

    st.header("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    st.markdown("---")

    st.subheader("Example Questions")

    st.write("Total sales")
    st.write("Average revenue")
    st.write("Highest sales")
    st.write("Lowest revenue")

# LOAD DATASET
if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_csv(uploaded_file, encoding="latin1")

    st.success("Dataset loaded successfully")

    # DATA METRICS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))

    st.markdown("### Dataset Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # CHAT SECTION
    st.subheader("Chat with your data")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask a question about the dataset...")

    if user_input:

        st.session_state.messages.append(("user", user_input))

        columns = df.columns.tolist()

        column = match_column(user_input, columns)
        group_col = detect_groupby(user_input, columns)

        response = ""

        if column:

            # AVERAGE
            if "average" in user_input.lower():

                result = df[column].mean()
                response = f"Average {column} is {round(result,2)}"

            # MAX
            elif "highest" in user_input.lower() or "max" in user_input.lower():

                result = df[column].max()
                response = f"Highest {column} is {result}"

            # MIN
            elif "lowest" in user_input.lower() or "min" in user_input.lower():

                result = df[column].min()
                response = f"Lowest {column} is {result}"

            # GROUP BY
            elif "by" in user_input.lower() and group_col:

                grouped = df.groupby(group_col)[column].sum().sort_values(ascending=False)

                response = f"{column} by {group_col}"

                fig = px.bar(
                    grouped,
                    title=f"{column} by {group_col}"
                )

                st.plotly_chart(fig, use_container_width=True)

            # SUM
            else:

                result = df[column].sum()
                response = f"Total {column} is {result}"

        else:

            response = "Sorry, I couldn't understand the query."

        st.session_state.messages.append(("bot", response))

    # DISPLAY CHAT
    for role, msg in st.session_state.messages:

        if role == "user":
            st.markdown(f'<div class="chat-user">{msg}</div>', unsafe_allow_html=True)

        else:
            st.markdown(f'<div class="chat-bot">{msg}</div>', unsafe_allow_html=True)

else:

    st.info("Upload a dataset from the sidebar to begin.")