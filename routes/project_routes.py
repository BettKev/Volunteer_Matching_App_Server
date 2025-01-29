from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Project  # Import models

project_routes = Blueprint('projects', __name__)

@project_routes.route('/projects', methods=['POST'])
@jwt_required()  # Require authentication
def create_project():
    # Get the logged-in user's ID from JWT token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # Check if the user exists and is an organization
    if not user or user.role != 'organization':
        return jsonify({'message': 'Unauthorized: Only organizations can create projects'}), 403

    # Get data from request
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    # Validate request data
    if not title or not description:
        return jsonify({'message': 'Title and description are required'}), 400

    # Create a new project
    new_project = Project(title=title, description=description, organization_id=user.user_id)

    # Save to database
    db.session.add(new_project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully', 'project_id': new_project.project_id}), 201
