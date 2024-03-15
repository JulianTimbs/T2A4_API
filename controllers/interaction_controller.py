from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.interaction import Interaction, interaction_schema, interactions_schema
from controllers.customer_controller import is_user_admin

interaction_bp = Blueprint('interactions', __name__,
                           url_prefix='/interactions')


@interaction_bp.route('/')
def get_all_interactions():
    stmt = db.select(Interaction).order_by(Interaction.date.desc())
    interactions = db.session.scalars(stmt)
    return interactions_schema.dump(interactions)


@interaction_bp.route('/<int:interaction_id>')
def get_one_interaction(interaction_id):
    stmt = db.select(Interaction).filter_by(id=interaction_id)
    interaction = db.session.scalar(stmt)
    if interaction:
        return interaction_schema.dump(interaction)
    else:
        return {'error': f'interaction with id {interaction_id} not found'}


@interaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_interaction():
    body_data = interaction_schema.load(request.get_json())
    interaction = Interaction(
        int_type=body_data.get('int_type'),
        date=date.today(),
        user_id=get_jwt_identity(),
        customer_id=body_data.get('customer_id')
    )
    db.session.add(interaction)
    db.session.commit()
    return interaction_schema.dump(interaction), 201


@interaction_bp.route('/<int:interaction_id>', methods=['DELETE'])
@jwt_required()
def delete_interaction(interaction_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'must be admin to delete an interaction'}
    stmt = db.select(Interaction).filter_by(id=interaction_id)
    interaction = db.session.scalar(stmt)
    if interaction:
        db.session.delete(interaction)
        db.session.commit()
        return {'message': 'interaction successfully deleted'}
    else:
        return {'error': f'interaction with id {interaction_id} not found'}


@interaction_bp.route('/<int:interaction_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_interaction(interaction_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'must be admin to update an interaction'}, 403
    body_data = interaction_schema.load(request.get_json(), partial=True)
    stmt = db.select(Interaction).filter_by(id=interaction_id)
    interaction = db.session.scalar(stmt)
    if interaction:
        interaction.int_type = body_data.get(
            'int_type') or interaction.int_type
        interaction.date = body_data.get('date') or interaction.date
        interaction.user_id = body_data.get('user_id') or interaction.user_id
        interaction.customer_id = body_data.get(
            'customer_id') or interaction.customer_id

        db.session.commit()
        return interaction_schema.dump(interaction)
    else:
        return {'error': f'interaction with id {interaction_id} not found'}, 404
