class MemberAlreadyRegisteredError(Exception):
    def __init__(self, message="Member is already registered for this class."):
        self.message = message
        super().__init__(self.message)
