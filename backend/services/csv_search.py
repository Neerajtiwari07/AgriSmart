import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "datasets", "agri_faq.csv")

faq_data = pd.read_csv(CSV_PATH)


def search_csv(user_question: str):

    user_question = user_question.strip().lower()

    for _, row in faq_data.iterrows():

        question = str(row["Question"]).strip().lower()

        if user_question == question:
            return row["Answer"]

    return None