from bugzilla.agents import BMOAgent
from server import create_db_connnection
import MySQLdb


#------------------------------------------------------------------------------
#
# This python module polls the bugs marked as 'investigating' in the
# database. It then polls bugzilla for the status of each bug, and builds
# a list of 'conflicts' where the bug is resolved on bugzilla, but not in the
# database
#
# @author: Samuel Shadwell (https://github.com/samshadwell)
#
#------------------------------------------------------------------------------

def bugzilla_status(bmo, bugid):
    """
    Checks the status of the given bugid on bugzilla

    INPUTS: bmo, an instance of the BMOAgent class (from bztools)
            bugid, the bugid of the bug to poll
    OUTPUT: a string corresponding to the status of the given bug on bugzilla
    """

    #Poll bugzilla for the bug
    options = {'id' : bugid}
    buglist = bmo.get_bug_list(options)

    #Get bug status and return
    status = ''
    for bug in buglist:
        status = bug.status

    return status


def get_investigating_bugs():
    """
    Builds a list of bugs for which the status is marked as 'investigating' 
    in the local database

    INPUTS: None
    OUTPUT: List of bugids which are marked as 'investigating'
    """

    #Get database connection
    db = create_db_connnection()
    cursor = db.cursor()

    #Query for the 'investigating' bugs
    query = "SELECT id WHERE status = 'investigating'"
    cursor.execute(query)

    #Append the bug id's to the list object to be returned
    buglist = []
    for bugid in cursor:
        buglist.append(bugid)

    return buglist


def get_conflicting_bugs():
    """
    Get a list of bugs for which their status is 'investigating' in the local
    database, but 'RESOLVED' at bugzilla

    INPUTS: None
    OUTPUT: List of bugids which are 'conflicting' as per the above definition
    """

    bmo = BMOAgent()
    conflicting = []

    #Get the local db bugs marked as 'investigating'
    investigating = get_investigating_bugs()
  
    #Check to see if any 'investigating' bugs are resolved on bugzilla
    for bugid in investigating:
        if (bugzilla_status(bmo, bugid) == 'RESOLVED'):
            conflicting.append(bugid)

    return conflicting

