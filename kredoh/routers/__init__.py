from typing import Dict, Optional

from google.cloud import firestore

debug = True


def store_to_firestore(ref: str, data: Dict, path: str, table_name: Optional[str] = 'CALLBACKS'):
    if debug:
        table_name += '-TEST'
    db = firestore.Client()
    doc_ref = db.collection(table_name.lower()).document(ref)
    doc = doc_ref.get()
    if not doc.exists:
        content = {'path': path,
                   'data': data,
                   'ref': ref}
        doc_ref.set(content)
        return True

    return False
