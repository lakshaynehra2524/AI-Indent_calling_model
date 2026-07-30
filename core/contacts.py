# Small static demo contact book - stands in for a real contacts API/device
# integration a browser app can't reach. Edit freely for your own demo.
CONTACTS = {
    "mom": "+15551234567",
    "dad": "+15551234568",
    "john": "+15551234569",
    "office": "+15551234570",
}


def lookup_contact(name):
    if not name:
        return None

    return CONTACTS.get(name.strip().lower())
