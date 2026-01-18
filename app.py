import streamlit as st
import pandas as pd
import tempfile
import os
import smtplib
from email.message import EmailMessage

from topsis_harditya_102303230.main import compute_topsis, validate_input_file


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


st.title("TOPSIS Decision Support Tool")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
weights = st.text_input("Enter weights (comma-separated)")
impacts = st.text_input("Enter impacts (+ or - , comma-separated)")
email = st.text_input("Enter email address")

if st.button("Run TOPSIS"):
    if not uploaded_file or not weights or not impacts or not email:
        st.error("All fields are required.")
    else:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, "input.csv")
                output_path = os.path.join(tmpdir, "output.csv")

                df = pd.read_csv(uploaded_file)
                df.to_csv(input_path, index=False)

                weight_list = [float(w) for w in weights.split(",")]
                impact_list = impacts.split(",")

                df = validate_input_file(input_path, weight_list, impact_list)
                scores = compute_topsis(df, weight_list, impact_list)

                df["Topsis Score"] = scores
                df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)
                df.to_csv(output_path, index=False)

                send_email(email, output_path)
                st.success("TOPSIS result emailed successfully!")

        except Exception as e:
            st.error(str(e))