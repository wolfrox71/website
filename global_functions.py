from flask import session

def validSessionID() -> bool:
    """Returns true if the session ID provided is valid for this session
    Returns False if not
        """
    
    # if the session does not exist/is none then return false as invalid
    if session is None:
        return False

    # if the sessionID is not in the session then it is invalid
    if ("sessionID" not in session):
        return False
    
    sessionID = session["sessionID"]

    # if the sessionID is the same as what should exist then the details are correct and the sessionID is valid
    if sessionID == generateSessionID():
        return True
    
    # if not return false as invalid
    return False


def generateSessionID() -> str:
    """Generate the sessionID for this session and return it as a string
    SessionID will be created by hashing(username+lastLoginTime) when implemented
    """

    # currently just return A as the username and lastLoginTime are not yet implemented
    sessionID = "A"

    # return the sessionID of the current user
    return sessionID
