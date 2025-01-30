from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, Application, User, Project

application_routes = Blueprint('application_routes', __name__)

# route for volunteer to apply for a project    
@application_routes.route('/projects/<int:project_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_project(project_id):
    """Allows a logged-in volunteer to apply for a project."""
    
    # Get the current user ID from the JWT token
    user_id = get_jwt_identity()
    
    # Fetch the user details
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # Ensure the user has the role of 'volunteer'
    if user.role != 'volunteer':
        return jsonify({"success": False, "message": "Only volunteers can apply for projects."}), 403

    # Check if the project exists
    project = Project.query.get(project_id)
    
    if not project:
        return jsonify({"success": False, "message": "Project not found."}), 404

    # Check if the user has already applied for this project
    existing_application = Application.query.filter_by(user_id=user_id, project_id=project_id).first()
    
    if existing_application:
        return jsonify({"success": False, "message": "You have already applied for this project."}), 400

    # Create a new application
    new_application = Application(user_id=user_id, project_id=project_id)
    db.session.add(new_application)
    db.session.commit()

    return jsonify({"success": True, "message": "Application submitted successfully!"}), 201
