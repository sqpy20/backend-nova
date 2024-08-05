import os
from flask import Blueprint, request, jsonify
from .model import User, Student_data, Predicted_score
from .extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import UnsupportedMediaType
import uuid
from .predictions.grade_prediction_model import GradePredictionModel


student_bp = Blueprint('student_bp', __name__)

# init the GradePredictionModel
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the paths to the pickle files
linear_regression_path = os.path.join(current_dir, 'predictions', 'pickle_files', 'linear_regression_model.pkl')
decision_tree_path = os.path.join(current_dir, 'predictions', 'pickle_files', 'decision_tree_model.pkl')

grade_model = GradePredictionModel(linear_regression_path, decision_tree_path)

# Student Registration
@student_bp.route('/api/student/register', methods=['POST'])
def student_register():
    """student Registeration Route for student

    Raises:
        UnsupportedMediaType: wrong content type

    Returns:
        JSON: {
                    "message": "User registered successfully",
                    "user": {
                        "access_token": "...........",
                        "email": "..........@yahoo.com",
                        "first_name": ".........",
                        "id": "...........",
                        "last_name": "..........",
                        "username": ".........."
                    }
                }
    """
    try:
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type in ['application/x-www-form-urlencoded', 'multipart/form-ddecision_tree_model.pklata', 'multipart/form-data; boundary=X-INSOMNIA-BOUNDARY']:
            data = request.form
        else:
            raise UnsupportedMediaType(f"Unsupported content type: {request.content_type}")

        required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Missing required field: {field}"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "User already exists"}), 400

        new_user = User(
            id=str(uuid.uuid4()),
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )

        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "username": new_user.username,
                "email": new_user.email,
                "access_token": access_token,
            }
        }), 201
    except UnsupportedMediaType as e:
        return jsonify({"message": str(e)}), 415
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Student Login
@student_bp.route('/api/student/login', methods=['POST'])
def student_login():
    """Login route for student

    Returns:
        JSON: {
                    "access_token": "...........",
                    "user": {
                        "email": "........@gmail.com",
                        "first_name": "......",
                        "last_name": "......",
                        "username": "......"
                    }
                }
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email
            }
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

# Submit Student Data
@student_bp.route('/api/student/data', methods=['POST'])
@jwt_required()
def submit_student_data():
    """Submit student data route for student

    Returns:
        JSON: {
                    "message": "Student data submitted successfully"
                }
    """
    data = request.get_json()
    student_id = get_jwt_identity()

    # Check if a record already exists for this student and course
    existing_data = Student_data.query.filter_by(
        student_id=student_id,
        course_name=data['course_name']
    ).first()

    if existing_data:
        # If both student_id and course_name match, return error
        return jsonify({"message": "Student data already exists for this course"}), 400

    # If we reach here, either student_id doesn't exist or course_name is different
    # So we create a new record
    new_student_data = Student_data(
        id=str(uuid.uuid4()),
        student_id=student_id,
        **data
    )
    db.session.add(new_student_data)

    try:
        db.session.commit()
        return jsonify({"message": "Student data submitted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Fetch all Student Data
@student_bp.route('/api/student/datas', methods=['GET'])
@jwt_required()
def get_student_data():
    """Fetch all student data route for student

    Returns:
        JSON: {
                "course_name": "........",
                "course_code": "........",
                "course_unit": "........",
                "test_score": "........",
                "exam_score": "........",
                "student_id": "........",
                "id": "........"
        }
    """
    student_id = get_jwt_identity()
    student_data_list = Student_data.query.filter_by(student_id=student_id).all()

    if not student_data_list:
        return jsonify({"message": "Student data not found"}), 404

    student_data_dicts = [student_data.to_dict() for student_data in student_data_list]

    return jsonify(student_data_dicts), 200

# predicting student data   
@student_bp.route('/api/student/create/prediction', methods=['POST'])
@jwt_required()
def create_student_prediction():
    """Create student prediction route for student

    Returns:
        JSON: {
            "message": "Prediction made successfully",
            "access_token": .........,
            "stored_prediction": {
                "course name": ".........",
                "decision tree pred class": .......,
                "decision tree pred prob": .....,
                "id": ".........",
                "linear regression pred": .........,
                "risk factor": "......",
                "student_data_id": "........"
            }
        }
    """
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if 'course_name' not in data:
        return jsonify({"message": "Course name is required"}), 400

    student_data = Student_data.query.filter_by(
        student_id=current_user,
        course_name=data['course_name']
        ).first()
    
    if not student_data:
        return jsonify({"message": "Student data not found"}), 404
    
    # Check if the student has a prediction for that course already
    existing_prediction = Predicted_score.query.filter_by(
        student_data_id=student_data.id,
        course_name=data['course_name']
    ).first()
    
    if existing_prediction:
        return jsonify({
            "message": "Prediction for this course already exists",
            "existing_prediction": existing_prediction.to_dict()
        }), 400
    
    try:
        # Convert student_data to a dictionary
        student_data_dict = student_data
        
        # Perform prediction
        predictions = grade_model.predict(student_data_dict)
        
        # Extract individual predictions
        decision_tree_pred_class = predictions['decision_tree']['predicted_class']
        decision_tree_pred_prob = predictions['decision_tree']['probability_distribution']
        risk_factor = predictions['risk_factor']
        linear_regression_pred = float(predictions['linear_regression'])
        
        # Create new Predicted_score entry
        new_prediction = Predicted_score(
            decision_tree_pred_class=decision_tree_pred_class,
            decision_tree_pred_prob=decision_tree_pred_prob,
            linear_regression_pred=linear_regression_pred,
            risk_factor=risk_factor,
            student_data_id=student_data.id,
            course_name=data['course_name']
        )
        
        db.session.add(new_prediction)
        db.session.commit()
        
        return jsonify({
            "message": "Prediction made successfully",
            "access_token": current_user,
            "stored_prediction": new_prediction.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": f"An error occurred: {str(e)}"
        }), 500

# get a specific student prediction for a specific course
@student_bp.route('/api/student/predictions', methods=['GET'])
@student_bp.route('/api/student/predictions/<string:course_name>', methods=['GET'])
@jwt_required()
def get_student_predictions(course_name: str=None):
    """Get student predictions route for student

    Args:
        course_name (str, optional): course name. Defaults to None.

    Returns:
        JSON: {
                    "predictions": [
                        {
                            "course name": ".........",
                            "course_name": ".........",
                            "decision tree pred class": .........,
                            "decision tree pred prob": .........,
                            "id": ".........",
                            "linear regression pred": .........,
                            "risk factor": ".........",
                            "student_data_id": "........."
                        }
                    ],
                    "user_id": "........."
                }
    """
    current_user = get_jwt_identity()
    
    # Base query
    query = Student_data.query.filter_by(student_id=current_user)
    
    # If course_name is provided, filter by it
    if course_name:
        query = query.filter_by(course_name=course_name)
    
    student_data_entries = query.all()
    
    if not student_data_entries:
        return jsonify({"message": "No student data found"}), 404
    
    all_predictions = []
    
    for student_data in student_data_entries:
        predicted_scores = Predicted_score.query.filter_by(student_data_id=student_data.id).all()
        
        for score in predicted_scores:
            prediction_dict = score.to_dict()
            prediction_dict['course_name'] = student_data.course_name
            all_predictions.append(prediction_dict)
    
    return jsonify({
        "user_id": current_user,
        "predictions": all_predictions
    }), 200


