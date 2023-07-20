
# Online Survey Platform
The Online Survey and Data Analysis Platform is a web application designed to facilitate the creation of custom surveys, collect responses, and perform data analysis through interactive visualizations and statistics. This platform is particularly useful for market researchers, businesses, and organizations seeking to gather valuable insights from their target audiences.

## Features
-Create Custom Surveys: Users can easily create surveys by providing a survey title and adding multiple questions. The platform offers a dynamic interface to add or remove questions on-the-fly, enabling users to design comprehensive surveys.

-Take Surveys: Participants can access and respond to the surveys created by users. The "Take Survey" feature displays the survey questions to respondents, allowing them to submit their responses efficiently.

-Visualize Survey Results: Powerful data visualization tools present survey results in an intuitive and insightful manner. Users can view responses to each survey question as well as aggregate statistics, facilitating the identification of trends and patterns.

-Remove Surveys and Questions: The platform provides an option to remove surveys and their associated questions when they are no longer required. This ensures data cleanliness and simplifies survey management.

-Database Integration: Surveys, questions, and responses are stored securely in an SQLite database, ensuring data integrity and persistence across sessions.

## Link to application : [Online Survey Application}(https://survey-platform-u7w37ndtkqj.streamlit.app/)
## Getting Started
Prerequisites
-Python 3.6 or higher
-Streamlit (Install using pip install streamlit)
-SQLite (No additional installation required as it comes built-in with Python)

## Installation
-Clone the repository:git clone https://github.com/shibanisankpal/Survey-Platform.git
cd Survey-Platform


-Run the application:
streamlit run app.py
The application will be accessible at http://localhost:8501 in your web browser.

Usage
-Create Survey: Select the "Create Survey" option from the sidebar. Provide a title for your survey and add multiple questions. Click on the "Add Survey" button to save the survey and questions to the database.

-Take Survey: Choose the "Take Survey" option from the sidebar. Select the survey you wish to take from the drop-down list. Fill out the responses to each question and click on the "Submit" button.

-View Survey Results: Navigate to the "View Survey Results" section to visualize the responses to each question for a selected survey.

-Remove Survey: In case a survey is no longer needed, you can remove it along with its associated questions by selecting the "Remove Survey" option and choosing the survey to remove from the drop-down list.

## Database Structure
The platform uses an SQLite database with the following structure:

-surveys: Stores survey details (id, title).
-questions: Stores survey questions (id, survey_id, question).
-responses: Stores survey responses (id, survey_id, question_id, response).
