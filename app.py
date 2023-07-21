import streamlit as st
import sqlite3
import matplotlib.pyplot as plt

def create_db():
    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()

    # Create the tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS surveys
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    survey_id INTEGER,
                    question TEXT,
                    FOREIGN KEY (survey_id) REFERENCES surveys(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS responses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    survey_id INTEGER,
                    question_id INTEGER,
                    response TEXT,
                    FOREIGN KEY (survey_id) REFERENCES surveys(id),
                    FOREIGN KEY (question_id) REFERENCES questions(id))''')

    conn.commit()
    conn.close()

def create_survey():
    st.header("Create Survey")
    survey_title = st.text_input("Enter Survey Title:")
    if "questions" not in st.session_state:
        st.session_state.questions = [("", 0)]  # Initialize the questions list with a blank question

    question_count = st.number_input("Enter the number of questions:", min_value=1, value=1, step=1)

    # Store the questions in the session_state
    if len(st.session_state.questions) != question_count:
        if question_count > len(st.session_state.questions):
            st.session_state.questions.extend([("", i+1) for i in range(question_count - len(st.session_state.questions))])
        else:
            st.session_state.questions = st.session_state.questions[:question_count]

    # Display the questions input fields
    for i in range(question_count):
        st.text(f"Question {i+1}:")
        question_text = st.text_input(f"Question Text", key=f"question_{i}", value=st.session_state.questions[i][0])
        st.button("Remove", key=f"remove_{i}")  # Add a "Remove" button for each question
        st.session_state.questions[i] = (question_text, i + 1)

    if st.button("Add Survey"):
        conn = sqlite3.connect("survey.db")
        cursor = conn.cursor()

        # Insert the survey into the database
        cursor.execute("INSERT INTO surveys (title) VALUES (?)", (survey_title,))
        survey_id = cursor.lastrowid

        # Insert the questions into the database
        for i in range(question_count):
            question_text = st.session_state.questions[i][0]
            cursor.execute("INSERT INTO questions (survey_id, question) VALUES (?, ?)", (survey_id, question_text))

        conn.commit()
        conn.close()
        st.success("Survey created successfully!")

    # Remove a question if the "Remove" button is clicked
    for i in range(question_count):
        if st.session_state[f"remove_{i}"]:
            del st.session_state.questions[i]
            break  # To avoid index out of range error when question_count is reduced

def take_survey():
    st.header("Take Survey")
    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()

    # Get the list of surveys
    cursor.execute("SELECT id, title FROM surveys")
    surveys = cursor.fetchall()
    survey_ids = [survey[0] for survey in surveys]
    survey_titles = [survey[1] for survey in surveys]
    selected_survey = st.selectbox("Select Survey", survey_titles)

    # Get the questions for the selected survey
    cursor.execute("SELECT id, question FROM questions WHERE survey_id=?", (survey_ids[survey_titles.index(selected_survey)],))
    questions = cursor.fetchall()
    question_ids = [question[0] for question in questions]
    question_texts = [question[1] for question in questions]

    # Collect responses for each question
    responses = []
    for i in range(len(question_texts)):
        response = st.text_input(question_texts[i])
        responses.append(response)

    if st.button("Submit"):
        # Insert responses into the database
        for i in range(len(question_ids)):
            cursor.execute("INSERT INTO responses (survey_id, question_id, response) VALUES (?, ?, ?)",
                           (survey_ids[survey_titles.index(selected_survey)], question_ids[i], responses[i]))
        conn.commit()
        conn.close()
        st.success("Survey submitted successfully!")

def view_results():
    st.header("View Survey Results")
    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()

    # Get the list of surveys
    cursor.execute("SELECT id, title FROM surveys")
    surveys = cursor.fetchall()
    survey_titles = [survey[1] for survey in surveys]
    selected_survey = st.selectbox("Select Survey", survey_titles)

    # Get the questions for the selected survey
    cursor.execute("SELECT id, question FROM questions WHERE survey_id=?", (surveys[survey_titles.index(selected_survey)][0],))
    questions = cursor.fetchall()
    question_ids = [question[0] for question in questions]
    question_texts = [question[1] for question in questions]

    # Display the responses for each question
    for i, question_text in enumerate(question_texts):
        st.subheader(f"Question {i+1}: {question_text}")
        cursor.execute("SELECT response FROM responses WHERE survey_id=? AND question_id=?",
                       (surveys[survey_titles.index(selected_survey)][0], question_ids[i]))
        responses = cursor.fetchall()
        if responses:
            response_values = [response[0] for response in responses]
            st.bar_chart(response_values)
        else:
            st.write("No responses for this question.")

    conn.close()



def remove_survey():
    st.header("Remove Survey")
    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()

    # Get the list of surveys
    cursor.execute("SELECT id, title FROM surveys")
    surveys = cursor.fetchall()
    survey_titles = [survey[1] for survey in surveys]
    selected_survey = st.selectbox("Select Survey to Remove", survey_titles)

    # Remove the selected survey and its questions from the database
    survey_id = surveys[survey_titles.index(selected_survey)][0]
    cursor.execute("DELETE FROM surveys WHERE id=?", (survey_id,))
    cursor.execute("DELETE FROM questions WHERE survey_id=?", (survey_id,))
    conn.commit()
    conn.close()

    st.success(f"Survey '{selected_survey}' and its questions removed successfully!")

def main():
    st.title("Online Survey and Data Analysis Platform")
    create_db()  # Initialize the database

    menu = ["Create Survey", "Take Survey", "View Survey Results", "Remove Survey"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Create Survey":
        create_survey()

    elif choice == "Take Survey":
        take_survey()

    elif choice == "View Survey Results":
        view_results()

    elif choice == "Remove Survey":
        remove_survey()

if __name__ == "__main__":
    main()
