from firebase_admin import firestore

def get_current_edition(db):
    edition_ref = db.collection('settings').document('newsletter')
    edition_doc = edition_ref.get()
    if edition_doc.exists:
        return edition_doc.to_dict().get('edition_number', 1)  # Default to 1 if not set
    else:
        edition_ref.set({'edition_number': 1})  # Initialize if not present
        return 1

def update_edition_number(db, current_edition):
    edition_ref = db.collection('settings').document('newsletter')
    edition_ref.update({'edition_number': current_edition + 1})

def ordinal(n):
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= n % 100 <= 13:
        suffix = 'th'
    else:
        suffix = suffixes.get(n % 10, 'th')
    return str(n) + suffix