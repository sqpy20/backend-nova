from grade_prediction_model import GradePredictionModel

class MockStudentData:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __iter__(self):
        return iter(self.__dict__.values())


# Create a mock student data object with sample data
student_data = MockStudentData(
    age=20,
    grade_level="Freshman",
    learning_style="Visual",
    socio_economic_status="Middle Income",
    past_grades=100,
    standardized_test_scores=1900,
    prior_knowledge="None",
    course_id=101,
    course_name="Advanced bilogy",
    course_difficulty="Hard",
    class_size=30,
    teaching_style="Lecture-based",
    course_work_load="Projects, Presentations",
    attendance=100,
    study_time=10,
    time_of_year="Spring Semester",
    extra_curricular_activities="Yes",
    health="Good",
    home_environment="Quiet",
    actual_grade="A",
    cgpa=3.8
)
 

linear_regression_model_path = 'pickle_files/linear_regression_model.pkl'
decision_tree_model_path = 'pickle_files/decision_tree_model.pkl'

# Instantiate the GradePredictionModel with the paths to the models
model = GradePredictionModel(linear_regression_model_path, decision_tree_model_path)

# Run predictions and print the results
predictions = model.predict(student_data)
print(" linear_regression: ", predictions['linear_regression'])
print("decision_tree: ",predictions['decision_tree']['probability_distribution'])
print("predicted: ",predictions['decision_tree']['predicted_class'])
print("risk factor: ",predictions['risk_factor'])
pred = float(predictions['linear_regression'])



