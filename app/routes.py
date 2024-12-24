from flask import Blueprint, jsonify, request
from .models import Lead, Contact, Interaction
from .schemas import LeadSchema, ContactSchema, InteractionSchema
from . import db
from datetime import datetime, timezone


main = Blueprint('main', __name__)

lead_schema = LeadSchema()
leads_schema = LeadSchema(many=True)
contact_schema = ContactSchema()
interaction_schema = InteractionSchema()

@main.route('/leads', methods=['GET', 'POST'])
def manage_leads():
    if request.method == 'POST':
        data = request.json
        try:
            # Convert next_call_date to a Python date object
            next_call_date = (
                datetime.strptime(data['next_call_date'], '%Y-%m-%d').date()
                if 'next_call_date' in data and data['next_call_date']
                else None
            )
            
            new_lead = Lead(
                name=data['name'],
                status=data.get('status', "New"),
                next_call_date=next_call_date
            )
            db.session.add(new_lead)
            db.session.commit()
            return jsonify(lead_schema.dump(new_lead)), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    leads = Lead.query.all()
    return jsonify(leads_schema.dump(leads))

@main.route('/contacts', methods=['POST'])
def add_contact():
    data = request.json
    new_contact = Contact(
        lead_id=data['lead_id'],
        name=data['name'],
        role=data.get('role'),
        phone=data['phone'],
        email=data['email']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(contact_schema.dump(new_contact)), 201

@main.route('/interactions', methods=['POST'])
def add_interaction():
    data = request.json
    new_interaction = Interaction(
        lead_id=data['lead_id'],
        details=data['details'],
        interaction_date=data.get('interaction_date', datetime.now(timezone.utc)),
        order_placed=data.get('order_placed', False)
    )
    db.session.add(new_interaction)
    db.session.commit()
    return jsonify(interaction_schema.dump(new_interaction)), 201

