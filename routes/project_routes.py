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


# Route to update project (Only organizations can update)
@project_routes.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()  # Require authentication
def update_project(project_id):
    # Get logged-in user's ID from JWT token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # Check if the user exists and is an organization
    if not user or user.role != 'organization':
        return jsonify({'message': 'Unauthorized: Only organizations can update projects'}), 403

    # Find the project by ID
    project = Project.query.get(project_id)

    if not project:
        return jsonify({'message': 'Project not found'}), 404

    # Check if the logged-in user is the owner of the project
    if project.organization_id != user.user_id:
        return jsonify({'message': 'Unauthorized: You can only update your own projects'}), 403

    # Get data from request
    data = request.get_json()
    title = data.get('title', project.title)  # Keep existing title if not provided
    description = data.get('description', project.description)  # Keep existing description if not provided
    status = data.get('status', project.status)  # Keep existing status if not provided

    # Update project details
    project.title = title
    project.description = description
    project.status = status

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'Project updated successfully', 'project_id': project.project_id}), 200


# Route to delete project (Only organizations can delete their own projects)
@project_routes.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()  # Require authentication
def delete_project(project_id):
    # Get logged-in user's ID from JWT token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # Check if the user exists and is an organization
    if not user or user.role != 'organization':
        return jsonify({'message': 'Unauthorized: Only organizations can delete projects'}), 403

    # Find the project by ID
    project = Project.query.get(project_id)

    if not project:
        return jsonify({'message': 'Project not found'}), 404

    # Check if the logged-in user is the owner of the project
    if project.organization_id != user.user_id:
        return jsonify({'message': 'Unauthorized: You can only delete your own projects'}), 403

    # Delete project from the database
    db.session.delete(project)
    db.session.commit()

    return jsonify({'message': 'Project deleted successfully'}), 200
