"""drafting and designing a manager for python written module.
the current plan is that there'll be a Manager that the PythonScriptModule
instanciates, and which then loads the python modules that are to be autoloaded,
and handles their event registrations, passing incoming events to them etc.
that will be prototyped here in pure py, and perhaps reused in the actual
impl if it seems that a py written manager makes sense within the c++ framework too.

currently here is also test code for modules and handelers that would
use the manager, nothing of the Manager itself yet.
"""

e = rexviewer.event

class TestModule:
    """A wish of how a py written module might like to have the system.
    This could for example be the CommunicationsModule, right?
    Or something that implements as a custom control type..
    Now attempting a generic test thing."""
    
    def __init__(self):
        self.data = 1
        
    @e.update
    def update(self):
        if self.data == 1:
            self.data == 0
        else:
            self.data == 1
            
"""
why not allow plain functions as event handlers too,
the python module of it, i.e. the file, can be considered as the module,
so no classes are required.
"""

@e.update
def dosomething():
    pass #e.g. move an objec w.r.t to something (like time?)
    
"""
update may be nice as a method, but the real thing are the events.
"""

@e.communication.PRESENCE_STATUS_UPDATE
def sparkle_presence_updates():
    """a custom visual thing: some local sparkles upon IM presence updates.
    what data do we have in these events? the im participant id?
    is that associated to an avatar anywhere? so could e.g. get the location..
    """
    create_sparkle((0,2, 0,2), 0.5) #in upper right corner, for half a sec

