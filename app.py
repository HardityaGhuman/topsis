import streamlit as st
import pandas as pd
import tempfile
import os
import smtplib
from email.message import EmailMessage

from topsis_harditya_102303230.main import compute_topsis, validate_input_file


# ------------------ SAMPLE CSV ------------------
SAMPLE_CSV = """Model,Cost,Performance,Battery,Weight
M1,250,70,12,1.8
M2,200,65,10,2.1
M3,300,80,14,1.6
M4,275,75,13,1.9
"""

st.title("TOPSIS Decision Support Tool")

st.download_button(
    label="Download Sample CSV",
    data=SAMPLE_CSV,
    file_name="sample_topsis_input.csv",
    mime="text/csv"
)


# ------------------ EMAIL FUNCTION ------------------
def send_email(receiver, file_path):
    try:
        sender = st.secrets["TOPSIS_EMAIL"]
        password = st.secrets["TOPSIS_PASSWORD"]
    except KeyError:
        raise Exception("Email credentials not set in Streamlit secrets")

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Please find the TOPSIS result attached.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="topsis_result.csv"
        )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)


# ------------------ INPUTS ------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ------------------ CSV PREVIEW ------------------
if uploaded_file is not None:
    try:
        preview_df = pd.read_csv(uploaded_file)
        st.subheader("Preview Input CSV")
        st.dataframe(preview_df.head())
    except Exception:
        st.error("Unable to preview CSV file. Please check the format.")
        
weights = st.text_input("Enter weights (comma-separated)")
impacts = st.text_input("Enter impacts (+ or -, comma-separated)")
email = st.text_input("Enter email address (optional)")


# ------------------ RUN TOPSIS ------------------
if st.button("Run TOPSIS"):
    if not uploaded_file or not weights or not impacts:
        st.error("CSV file, weights, and impacts are required.")
    else:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "input.csv")
                output_path = os.path.join(tmpdir, "output.csv")

                df = pd.read_csv(uploaded_file)
                df.to_csv(input_path, index=False)

                weight_list = [float(w.strip()) for w in weights.split(",")]
                impact_list = [i.strip() for i in impacts.split(",")]

                df = validate_input_file(input_path, weight_list, impact_list)
                scores = compute_topsis(df, weight_list, impact_list)

                df["Topsis Score"] = scores
                df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)
                df.to_csv(output_path, index=False)

                # ---- SHOW RESULTS ON PAGE ----
                st.subheader("TOPSIS Results")
                st.dataframe(df)

                st.download_button(
                    label="Download Result CSV",
                    data=df.to_csv(index=False),
                    file_name="topsis_result.csv",
                    mime="text/csv"
                )

                if email.strip():
                    send_email(email, output_path)
                    st.success("TOPSIS result emailed successfully!")
                else:
                    st.success("TOPSIS computation completed successfully!")

        except Exception as e:
            st.error(str(e))