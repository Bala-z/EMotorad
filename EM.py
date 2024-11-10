from flask import Flask, request, jsonify
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import enum

app = Flask(__name__)

# Connecting MySQL database
DATABASE_URI = 'mysql+pymysql://root:new_password@localhost/Emotorad'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the Contact model based on the MySQL table schema
class LinkPrecedenceEnum(enum.Enum):
    primary = "primary"
    secondary = "secondary"

class Contact(Base):
    __tablename__ = 'Contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phoneNumber = Column(String(15), nullable=True)
    email = Column(String(255), nullable=True)
    linkedId = Column(Integer, ForeignKey('Contacts.id'), nullable=True)
    linkPrecedence = Column(Enum(LinkPrecedenceEnum), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

# Table creation
Base.metadata.create_all(engine)

# Define the /identify endpoint
@app.route('/identify', methods=['POST'])
def identify():
    data = request.get_json()
    email = data.get("email")
    phone_number = data.get("phoneNumber")
    
    # Search for existing contacts with the same email or phone number
    existing_contacts = session.query(Contact).filter(
        (Contact.email == email) | (Contact.phoneNumber == phone_number)
    ).all()

    if not existing_contacts:
        # If no matching contact, create a new primary contact
        new_contact = Contact(email=email, phoneNumber=phone_number, linkPrecedence="primary")
        session.add(new_contact)
        session.commit()
        response = {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }
    else:
        # If matching contacts found, consolidate information
        primary_contact = next((contact for contact in existing_contacts if contact.linkPrecedence == "primary"), None)
        
        if not primary_contact:
            primary_contact = existing_contacts[0]
            primary_contact.linkPrecedence = "primary"
        
        # Consolidate emails and phone numbers
        emails = {contact.email for contact in existing_contacts if contact.email}
        phone_numbers = {contact.phoneNumber for contact in existing_contacts if contact.phoneNumber}
        
        if (email and email not in emails) or (phone_number and phone_number not in phone_numbers):
            # Add secondary contact if new information is provided
            secondary_contact = Contact(
                email=email, phoneNumber=phone_number, linkedId=primary_contact.id, linkPrecedence="secondary"
            )
            session.add(secondary_contact)
            session.commit()
            existing_contacts.append(secondary_contact)
        
        response = {
            "primaryContactId": primary_contact.id,
            "emails": list(emails),
            "phoneNumbers": list(phone_numbers),
            "secondaryContactIds": [contact.id for contact in existing_contacts if contact.linkPrecedence == "secondary"]
        }
        
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
