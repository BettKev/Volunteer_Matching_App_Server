from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, User, Project  # Import models

project_routes = Blueprint('projects', __name__)

@project_routes.route('/projects', methods=['POST'])
@jwt_required()  # Require authentication
def create_project():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'organization':
        return jsonify({'message': 'Unauthorized: Only organizations can create projects'}), 403
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({'message': 'Title and description are required'}), 400
    
    new_project = Project(title=title, description=description, organization_id=user.user_id)
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify({'message': 'Project created successfully', 'project_id': new_project.project_id}), 201

@project_routes.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'organization':
        return jsonify({'message': 'Unauthorized: Only organizations can update projects'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    if project.organization_id != user.user_id:
        return jsonify({'message': 'Unauthorized: You can only update your own projects'}), 403
    
    data = request.get_json()
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    
    db.session.commit()
    return jsonify({'message': 'Project updated successfully', 'project_id': project.project_id}), 200

@project_routes.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'organization':
        return jsonify({'message': 'Unauthorized: Only organizations can delete projects'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    
    if project.organization_id != user.user_id:
        return jsonify({'message': 'Unauthorized: You can only delete your own projects'}), 403
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

# New route to fetch all projects (Accessible to any authenticated user)
@project_routes.route('/projects', methods=['GET'])
@jwt_required()
def get_all_projects():
    projects = Project.query.all()
    
    project_list = [
        {
            'project_id': project.project_id,
            'title': project.title,
            'description': project.description,
            'organization_id': project.organization_id,
            'status': project.status
        } 
        for project in projects
    ]
    
    return jsonify({'projects': project_list}), 200
