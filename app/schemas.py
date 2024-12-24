from . import ma
from .models import Lead, Contact, Interaction

class LeadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lead
        include_relationships = True
        load_instance = True


class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        load_instance = True


class InteractionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Interaction
        load_instance = True

