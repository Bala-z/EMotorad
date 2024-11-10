# EMotorad
# Project Description
This web service is designed to process customer orders and consolidate contact information across multiple purchases, effectively recognizing different orders from the same individual. This helps link orders under a single profile, even if the customer uses different emails and phone numbers each time.
The service includes:

1. A /identify endpoint that accepts JSON payloads containing "email" and "phoneNumber" fields.
2. A response that provides a consolidated profile, showing the primary contact and associated emails, phone numbers, and secondary contacts.

Requirements
* Python 3.x
* Flask
* SQLAlchemy
* pymysql

Steps:-
1. Clone the repository
2. Install dependencies
3. Set Up the Database
4. Run the service

Work Flow:-
* Primary and Secondary Contacts: When a contact doesn’t exist, the service creates a new “primary” contact. If a matching contact is found, a “secondary” contact is linked to an existing primary one.
* Dynamic Linking: The system can adaptively reassign contacts between primary and secondary, based on the new information it receives.
* Unified Response: The service offers a single view of all emails and phone numbers associated with an individual’s profile.
