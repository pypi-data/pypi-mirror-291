class HubException(Exception):
    """The base exception for all Hub issues"""

    pass


class OrganizationException(HubException):
    """The base exception for all Hub Organization issues"""

    pass


class ClosedOrganizationRegistrationException(OrganizationException):
    """New organizations cannot be registered anymore"""

    pass


class DisabledOrganizationException(OrganizationException):
    """The requested organization has been disabled from the platform"""

    pass


class DuplicateOrganizationException(OrganizationException):
    """An organization with the same NGO Hub ID already exists"""

    pass


class MissingOrganizationException(OrganizationException):
    """The requested organization does not exist"""

    pass


class HubHTTPException(HubException):
    """The base exception for all Hub HTTP/network issues"""

    pass


class HubDecodeException(HubHTTPException):
    """Failed to decode response"""

    pass
