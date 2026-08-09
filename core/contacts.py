# Small static demo contact book - stands in for a real contacts API/device
# integration a browser app can't reach. Edit freely for your own demo.



def lookup_contact(name):
    if not name:
        return None

    return CONTACTS.get(name.strip().lower())
