import pickle
import pandas as pd


class GradePredictionModel:
    def __init__(self, linear_regression_path, decision_tree_path):
        self.linear_regression_model = self.load_model(linear_regression_path)
        self.decision_tree_model = self.load_model(decision_tree_path)
        self.feature_order = [
            'Age', 'Grade Level', 'Learning Style', 'Socio Economic Status',
            'Past Grades', 'Standardized Test Scores', 'Prior Knowledge',
            'Course ID', 'Course Name', 'Course Difficulty', 'Class Size',
            'Teaching Style', 'Course Work Load', 'Attendance', 'Study Time',
            'Time of Year', 'Extra Curricular Activities', 'Health',
            'Home Environment', 'Actual Grade', 'CGPA'
        ]
        self.grade_mapping = {
            "A+": 4, "A": 4, "A-": 4,
            "B+": 3, "B": 3, "B-": 3,
            "C+": 2, "C": 2, "C-": 2,
            "D+": 1, "D": 1, "D-": 1,
            "F": 0
        }


    @staticmethod
    def load_model(model_path):
        """Loads the pickled model from the specified path."""
        with open(model_path, 'rb') as f:
            return pickle.load(f)


    def clean_data(self, student_data):
        """Cleans and processes the student data for prediction."""
        cleaned_data = {}

        # Lowercase and replace spaces with underscores for attribute names
        attribute_map = {field.lower().replace(' ', '_'): field for field in self.feature_order}

        # Check if all required fields are present (case-insensitive)
        missing_fields = [field for field in self.feature_order if field.lower().replace(' ', '_') not in student_data.__dict__]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        for field in self.feature_order:
            attribute_name = field.lower().replace(' ', '_')
            value = getattr(student_data, attribute_name, None)
            try:
                # Handle specific fields
                if field == 'actual_grade':
                    # If actual_grade is already a number, use it directly
                    if isinstance(value, (int, float)):
                        cleaned_data[field] = float(value)
                    else:
                        # If it's a letter grade, map it to a number
                        cleaned_data[field] = self.grade_mapping.get(value, 0)
                elif field in ['age', 'class_size', 'attendance', 'study_time', 'course_id', 'standardized_test_scores']:
                    cleaned_data[field] = int(value) if value is not None else 0
                elif field in ['past_grades', 'cgpa']:
                    cleaned_data[field] = float(value) if value is not None else 0.0
                elif field == 'extra_curricular_activities':
                    cleaned_data[field] = 1 if value else 0  # Assuming it's a boolean
                else:
                    # Keeps everything else as strings
                    cleaned_data[field] = str(value) if value is not None else ''
            except (ValueError, TypeError) as e:
                # Handle conversion errors or unexpected data types
                print(f"Error processing field '{field}': {e}")
                # Consider assigning default values or removing the data point
        
        return cleaned_data


    def predict_grade_linear_regression(self, processed_data):
        """Predicts a student's grade using the linear regression model."""
        prediction = self.linear_regression_model.predict(processed_data)
        return prediction[0]


    def predict_grade_decision_tree(self, processed_data):
        """Predicts a student's grade using the decision tree model."""
        probabilities = self.decision_tree_model.predict_proba(processed_data)[0]
        threshold = 0.6  # Adjust threshold as needed
        predicted_class = "Pass" if probabilities[1] >= threshold else "Fail"
        return predicted_class, probabilities.tolist()


    def predict(self, student_data):
        """Predicts a student's grade using both linear regression and decision tree models.

        Args:
            student_data: An object containing student data with attributes matching the feature order.

        Returns:
            A dictionary containing the predictions from both models.
        """

        cleaned_data = self.clean_data(student_data)

        # Convert cleaned data to a Pandas DataFrame for flexibility
        df = pd.DataFrame(cleaned_data, index=[0])

          # Define your column mapping
        column_mapping = {
            'age': 'Age',
            'cgpa': 'cgpa',
            'extra_curricular_activities': 'Extracurricular Activities',
            'past_grades' : 'Past Grades',
            'standardized_test _scores' : 'Standardized Test Scores',
            'class_size' : 'Class Size',
            'attendance' : 'Attendance',
            'study_time' : 'Study Time',
            'grade_level' : 'Grade Level',
            'learning_style' : 'Learning Style',
            'socio_economic_status' : 'Socioeconomic Status',
            'course_id' : 'Course ID',
            'course_name' : 'Course Name',
            'course_difficulty' : 'Course Difficulty',
            'course_work_load' : 'Coursework Load',
            'time_of_year' : 'Time of Year',
            'health' : 'Health',
            'home_environment' : 'Home Environment',
            'actual_grade' : 'Actual Grade',
            'teaching_style' : 'Teaching Style',
        }
         # this is adding the CGPA
        df.rename(columns={'CGPA': 'cgpa'}, inplace=True)

        # Apply the mapping to the DataFrame
        df = df.rename(columns=column_mapping)
        
        # Preprocess data for linear regression (adjust based on your training pipeline)
        linear_regression_data = df[["Age", "Past Grades", "Standardized Test Scores",
            "Class Size", "Attendance", "Study Time", "cgpa"]]
        
        # Convert to NumPy array
        linear_regression_data = linear_regression_data.values 

        feature_names = ['Student ID', 'Age', 'Past Grades', 'Standardized Test Scores', 'Course ID', 'Class Size', 'Attendance', 'Study Time', 'cgpa', 'Learning Style_Auditory', 'Learning Style_Kinesthetic', 'Learning Style_Visual', 'Course Name_Advanced Biology', 'Course Name_Advanced Biology Lab', 'Course Name_Advanced Calculus', 'Course Name_Advanced Calculus I', 'Course Name_Advanced Chemistry', 'Course Name_Advanced Chemistry Lab', 'Course Name_Advanced Economics', 'Course Name_Advanced Literature', 'Course Name_Advanced Math', 'Course Name_Advanced Mathematics', 'Course Name_Advanced Philosophy', 'Course Name_Advanced Physics', 'Course Name_Advanced Physics I', 'Course Name_Advanced Physics Lab', 'Course Name_Advanced Psychology', 'Course Name_Advanced Sociology', 'Course Name_Advanced Statistics', 'Course Name_Calculus I', 'Course Name_Calculus II', 'Course Name_Calculus III', 'Course Name_Calculus IV', 'Course Name_Calculus V', 'Course Name_Chemistry I', 'Course Name_College Algebra', 'Course Name_College Algebra II', 'Course Name_College Algebra II Introduction to Algebra II', 'Course Name_College Algebra III', 'Course Name_College Algebra III (Algebra III)', 'Course Name_College Algebra III Introduction to Algebra III', 'Course Name_College Algebra IV', 'Course Name_College Algebra IV Introduction to Algebra IV', 'Course Name_College Biology I Introduction to Biology', 'Course Name_College Biology I Introduction to Biology I', 'Course Name_College Biology II Introduction to Biology I', 'Course Name_College Biology II Introduction to Biology II', 'Course Name_College Biology III (Biology III)', 'Course Name_College Biology III Introduction to Biology III', 'Course Name_College Biology IV Introduction to Biology IV', 'Course Name_College Literature I Introduction to Literature I', 'Course Name_College Literature II', 'Course Name_College Literature II Introduction to Literature II', 'Course Name_College Literature III', 'Course Name_College Literature III Introduction to Literature III', 'Course Name_College Literature IV Introduction to Literature IV', 'Course Name_College US History II (US History II)', 'Course Name_College US History II (US History)', 'Course Name_College US History III (US History III)', 'Course Name_College US History III (US History)', 'Course Name_College US History IV (US History IV)', 'Course Name_Data Analysis I', 'Course Name_English Composition', 'Course Name_English Literature II', 'Course Name_Fundamentals of Psychology', 'Course Name_Intermediate Anthropology', 'Course Name_Intermediate Art History', 'Course Name_Intermediate Biology', 'Course Name_Intermediate Chemistry', 'Course Name_Intermediate Economics', 'Course Name_Intermediate History', 'Course Name_Intermediate Physics', 'Course Name_Intermediate Psychology', 'Course Name_Intermediate Sociology', 'Course Name_Intermediate Spanish', 'Course Name_Introduction to Anthropology', 'Course Name_Introduction to Art', 'Course Name_Introduction to Art History', 'Course Name_Introduction to Astronomy', 'Course Name_Introduction to Biology', 'Course Name_Introduction to Chemistry', 'Course Name_Introduction to Computer Science', 'Course Name_Introduction to Economics', 'Course Name_Introduction to English Literature', 'Course Name_Introduction to Geology', 'Course Name_Introduction to History', 'Course Name_Introduction to Linguistics', 'Course Name_Introduction to Literature', 'Course Name_Introduction to Mathematics', 'Course Name_Introduction to Music Theory', 'Course Name_Introduction to Philosophy', 'Course Name_Introduction to Physics', 'Course Name_Introduction to Political Science', 'Course Name_Introduction to Psychology', 'Course Name_Introduction to Sociology', 'Course Name_Introduction to Statistics', 'Course Name_Introduction to World History', 'Course Name_Physics I', 'Course Name_Physics II', 'Course Name_Statistics I', 'Course Name_World History I', 'Course Name_World History II', 'Course Difficulty_Easy', 'Course Difficulty_Hard', 'Course Difficulty_Medium', 'Teaching Style_Activity-based', 'Teaching Style_Interactive', 'Teaching Style_Lecture-based', 'Grade Level_Freshman', 'Grade Level_Junior', 'Grade Level_Senior', 'Grade Level_Sophomore']

        # Identify missing features
        missing_features = set(feature_names) - set(df.columns)

        # Fill missing features with zeros (adjust as needed)
        for feature in missing_features:
            df[feature] = 0

        # Ensure feature order matches feature_names
        df = df[feature_names]
        
        # Make for linear regresssion predictions
        linear_regression_prediction = self.linear_regression_model.predict(linear_regression_data)[0]
        
        # Make for decision_tree_prediction predictions
        decision_tree_prediction, probabilities = self.decision_tree_model.predict_proba(df)[0]
        
        prediction_risk_factor = linear_regression_prediction
        
        risk_factor = None

        if (prediction_risk_factor > 3.5):
            risk_factor = "Not at risk"
        elif (prediction_risk_factor >= 3.0):
            risk_factor = "Risky"
        else:
            risk_factor = "At risk"
        
        return {
            "linear_regression": linear_regression_prediction,
            "risk_factor": risk_factor,
            "decision_tree": {
                "predicted_class": decision_tree_prediction,
                "probability_distribution": probabilities
            }
        }


  