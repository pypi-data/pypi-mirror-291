"""
This file has been auto generated from EVVA Airkey swagger file
(https://integration.api.airkey.evva.com/docs/swagger.json).
The content is subject to the original legal clauses. The author of
this project declines any responsibility for unlawful or unintended
use with respect to the original authors.

    EVVA AirKey Cloud API v18.0.4
    Terms of service: https://www.evva.com/en/airkey/impressum/
    Contacts: Contact https://airkey.evva.com
    License: Legal Notice https://www.evva.com/en/airkey/impressum/
    Host/Path: integration.api.airkey.evva.com:443/cloud
"""

from requests import Request


base_url = "https://integration.api.airkey.evva.com:443/cloud"


def get_admins():
    """
    Gets all access control operators.

    Returns a list of all access control operators defined in the access control
    system.

    Performs: GET /v1/acos

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/acos"

    return Request("GET", path)


def get_support_enabled_acos():
    """
    Gets all support logins.

    Returns a list of all support logins defined in the access control system.

    Performs: GET /v1/acos/support

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/acos/support"

    return Request("GET", path)


def get_areas(lock_id=None, offset=None, limit=None):
    """
    Gets all available areas.

    Returns a list of all available areas defined in the access control system,
    sorted by area id in ascending order.

    Performs: GET /v1/areas

    Parameters:
    lock_id -- (query:lockId) Filter areas by lock id

    offset  -- (query) Offset for paging

    limit   -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/areas"

    query = {
        "lockId": lock_id,
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_area(area_id):
    """
    Gets a specific area.

    Returns a specific area defined in the access control system.

    Performs: GET /v1/areas/{areaId}

    Parameters:
    area_id -- (path:areaId) Unique identifier of the area

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Area not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/areas/{area_id}"

    return Request("GET", path)


def get_authorizations(offset=None, limit=None, lock_id=None, area_id=None, medium_id=None, person_id=None):
    """
    Gets all authorizations for locks and areas.

    Returns a list of all authorizations for locks and areas defined in the access
    control system, sorted by 'created on' timestamp in descending order.

    Performs: GET /v1/authorizations

    Parameters:
    offset    -- (query) Offset for paging

    limit     -- (query) Limit of result size

    lock_id   -- (query:lockId) Filter authorizations by lock id

    area_id   -- (query:areaId) Filter authorizations by area id

    medium_id -- (query:mediumId) Filter authorizations by medium id

    person_id -- (query:personId) Filter authorizations by person id

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/authorizations"

    query = {
        "offset": offset,
        "limit": limit,
        "lockId": lock_id,
        "areaId": area_id,
        "mediumId": medium_id,
        "personId": person_id,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def delete_authorization(body):
    """
    Requests deletion of provided authorizations.

    Requests and marks provided authorizations for deletion and returns a list of
    the new authorization object versions.

    Performs: PUT /v1/authorizations

    Parameters:
    body -- (body) Authorizations to be deleted

    Response:
    (200) successful operation
    (400) Bad request
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Authorization to be deleted not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/authorizations"

    return Request("PUT", path, json=body)


def create_or_update_authorizations_with_advanced_options(body):
    """
    Creates new and updates existing authorizations (advanced version - can be used
    to create/update all types of authorizations).

    Creates the provided authorizations to be added in the access control system,
    updates the provided existing authorizations and returns a list of the new
    authorization object versions.
     The dates and timestamps for the authorizations should always be provided
    regardless of the time zone.
    Create authorization: Either lockId or areaId needs to be set for an
    authorization. It's not possible to set both IDs at the same time.
    Update authorization: It's not possible to change a lockId/areaId

    Performs: POST /v1/authorizations/advanced

    Parameters:
    body -- (body) Authorizations to be created or updated

    Response:
    (200) successful operation
    (400) Bad request
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Authorization to be updated not found
    (409) Authorization of medium for the provided lock/area already exists
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/authorizations/advanced"

    return Request("POST", path, json=body)


def create_or_fetch_simple_authorization(body):
    """
    Creates simple authorizations

    Creates an authorization of type 'SIMPLE' (same as using SimpleAuthorizationInfo
    in POST /authorizations/advanced). If an authorization can’t be created (e.g.
    already has 8 authorizations), an error will be returned. Be advised that this
    is only a simplified interface for fulfilling basic authorization needs, a
    'SIMPLE' authorization will actually consist of up to 3 AuthorizationInfo
    elements combined (of type one-day and permanent) within an authorization ->
    authorization of type 'SIMPLE' will never be part of a response.
    The dates and timestamps for the authorizations should always be provided
    regardless of the time zone.
    Either lockId or areaId needs to be set for an authorization. It's not possible
    to set both IDs at the same time.

    Performs: POST /v1/authorizations/simple

    Parameters:
    body -- (body) Authorization to be created

    Response:
    (200) successful operation
    (400) Bad request
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/authorizations/simple"

    return Request("POST", path, json=body)


def get_authorization(authorization_id):
    """
    Gets a specific authorization.

    Returns a specific authorization for locks and areas defined in the access
    control system.

    Performs: GET /v1/authorizations/{authorizationId}

    Parameters:
    authorization_id -- (path:authorizationId) Unique identifier of the
                        authorization

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Authorization not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/authorizations/{authorization_id}"

    return Request("GET", path)


def get_blacklists(lock_id=None, medium_id=None):
    """
    Gets all available blacklist entries.

    Returns a list of all available blacklist entries defined in the access control
    system, sorted by lock id and medium id in ascending order.

    Performs: GET /v1/blacklists

    Parameters:
    lock_id   -- (query:lockId) Filter blacklist entries by lock id

    medium_id -- (query:mediumId) Filter blacklist entries by medium id

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/blacklists"

    query = {
        "lockId": lock_id,
        "mediumId": medium_id,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_credits():
    """
    Gets available credit information.

    Returns information about available credits of customer.

    Performs: GET /v1/credits

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/credits"

    return Request("GET", path)


def get_credits_protocol(id=None, user_id=None, administrator=None, language='de-DE'):
    """
    Gets protocol of credits.

    Returns the protocol of credits actions

    Performs: GET /v1/credits-protocol

    Parameters:
    id            -- (query) Filter events by unique protocol entry identifier

    user_id       -- (query:userId) Filter events by unique administrator user
                     identifier

    administrator -- (query) Filter events by name of administrator

    language      -- (query) Language codes as a comma-separated list of IETF
                     (bcp47) language tags (e.g. de-DE, en-UK) or "all" for all
                     possible languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/credits-protocol"

    query = {
        "id": id,
        "userId": user_id,
        "administrator": administrator,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_customer_data():
    """
    Gets customer details.

    Returns stored data of the customer.

    Performs: GET /v1/customer

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/customer"

    return Request("GET", path)


def get_events(created_after, type=None, offset=None, limit=None):
    """
    Gets a list of events.

    Returns a list of events (only returns events that are max. 7 days old), sorted
    by event creation timestamp in descending order. Integration environment: 7 day
    restriction is not enforced, use '2019-04-28T00:00Z' as 'createdAfter' query
    parameter to get all events.

    Performs: GET /v1/events

    Parameters:
    created_after -- (query:createdAfter) Filter events that were created after this
                     timestamp (ISO 8601-format compliant date with time in UTC,
                     milliseconds precision: yyyy-mm-ddThh:mm:ss.SSSZ). Query
                     parameter is required because clients are encouraged to make a
                     choice what data is actually needed (e.g. when polling this
                     resource with an interval of 10 minutes: (createdAfter = now -
                     10 minutes) retrieves events which were created in the last 10
                     minutes.

    type          -- (query) Filter events by event type

    offset        -- (query) Offset for paging

    limit         -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/events"

    query = {
        "createdAfter": created_after,
        "type": type,
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_event(event_id):
    """
    Gets a specific event.

    Returns information about a specific event.

    Performs: GET /v1/events/{eventId}

    Parameters:
    event_id -- (path:eventId) Unique identifier of the event

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Event not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/events/{event_id}"

    return Request("GET", path)


def get_holiday_calendars():
    """
    Gets all holiday calendars.

    Returns all available holiday calendars defined in the access control system,
    sorted by holiday calendar id in ascending order.

    Performs: GET /v1/holiday-calendars

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars"

    return Request("GET", path)


def get_holiday_calendar(holiday_calendar_id):
    """
    Gets a specific holiday calendar.

    Returns information about a specific holiday calendar defined in the access
    control system.

    Performs: GET /v1/holiday-calendars/{holidayCalendarId}

    Parameters:
    holiday_calendar_id -- (path:holidayCalendarId) Unique identifier of the holiday
                           calendar

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}"

    return Request("GET", path)


def update_holiday_calendar(holiday_calendar_id, body):
    """
    Activates or deactivates the holiday calendar.

    Set the active flag within the HolidayCalendar model (body) to your desired
    value to activate or deactivate the holiday calendar. This is the only supported
    operation. Returns the updated holiday calendar object version.

    Performs: PUT /v1/holiday-calendars/{holidayCalendarId}

    Parameters:
    holiday_calendar_id -- (path:holidayCalendarId) Unique identifier of the holiday
                           calendar to be activated/deactivated

    body                -- (body) Holiday calendar to be activated/deactivated

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}"

    return Request("PUT", path, json=body)


def get_locks_by_calendar_id(holiday_calendar_id, offset=None, limit=None):
    """
    Gets all locks using the holiday calendar.

    Returns a list of all locks that are currently using the provided holiday
    calendar.

    Performs: GET /v1/holiday-calendars/{holidayCalendarId}/locks

    Parameters:
    holiday_calendar_id -- (path:holidayCalendarId) Unique identifier of the holiday
                           calendar

    offset              -- (query) Offset for paging

    limit               -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}/locks"

    query = {
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def create_holiday_calendar_slot(holiday_calendar_id, body):
    """
    Adds a new holiday calendar slot to the holiday calendar.

    Creates and adds the holiday calendar slot to the provided holiday calendar and
    returns the updated holiday calendar object version. In case of a series
    definition in the given holiday calendar slot, more than one holiday calendar
    slots could be created. To retrieve the newly created slots from the returned
    calendar, they can be filtered based on given slot name.

    Performs: POST /v1/holiday-calendars/{holidayCalendarId}/slots

    Parameters:
    holiday_calendar_id -- (path:holidayCalendarId) Unique identifier of the holiday
                           calendar with which the holiday calendar slot should be
                           associated

    body                -- (body) Holiday calendar slot to be added

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}/slots"

    return Request("POST", path, json=body)


def get_holiday_calendar_slot(holiday_calendar_id, holiday_calendar_slot_id):
    """
    Gets a specific holiday calendar slot.

    Returns information about a specific holiday calendar slot of the holiday
    calendar.

    Performs: GET /v1/holiday-calendars/{holidayCalendarId}/slots/{holidayCalendarSlotId}

    Parameters:
    holiday_calendar_id      -- (path:holidayCalendarId) Unique identifier of the
                                holiday calendar with which the holiday calendar
                                slot is associated

    holiday_calendar_slot_id -- (path:holidayCalendarSlotId) Unique identifier of
                                the holiday calendar slot

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar slot not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}/slots/{holiday_calendar_slot_id}"

    return Request("GET", path)


def update_holiday_calendar_slot(holiday_calendar_id, holiday_calendar_slot_id, body):
    """
    Updates a holiday calendar slot of the holiday calendar.

    Updates the provided holiday calendar slot and returns the new holiday calendar
    object version.

    Performs: PUT /v1/holiday-calendars/{holidayCalendarId}/slots/{holidayCalendarSlotId}

    Parameters:
    holiday_calendar_id      -- (path:holidayCalendarId) Unique identifier of the
                                holiday calendar with which the holiday calendar
                                slot is associated

    holiday_calendar_slot_id -- (path:holidayCalendarSlotId) Unique identifier of
                                the holiday calendar slot to be updated

    body                     -- (body) Holiday calendar slot to be updated

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar or slot not found
    (409) Conflict - holiday calendar slot has been changed
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}/slots/{holiday_calendar_slot_id}"

    return Request("PUT", path, json=body)


def delete_holiday_calendar_slot(holiday_calendar_id, holiday_calendar_slot_id, body):
    """
    Deletes provided holiday calendar slot.

    Deletes the provided holiday calendar slot and returns the new holiday calendar
    object version.

    Performs: DELETE /v1/holiday-calendars/{holidayCalendarId}/slots/{holidayCalendarSlotId}

    Parameters:
    holiday_calendar_id      -- (path:holidayCalendarId) Unique identifier of the
                                holiday calendar with which the holiday calendar
                                slot is associated

    holiday_calendar_slot_id -- (path:holidayCalendarSlotId) Unique identifier of
                                the holiday calendar slot to be deleted

    body                     -- (body) Holiday calendar slot to be deleted

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, wrong data type supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Holiday calendar or slot not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/holiday-calendars/{holiday_calendar_id}/slots/{holiday_calendar_slot_id}"

    return Request("DELETE", path, json=body)


def get_lock_protocol(offset=None, limit=None, area_id=None, lock_id=None, from_ts=None, to_ts=None, language='de-DE'):
    """
    Deprecated/Legacy: This resource will be removed in future versions. Please use
    resource "/v1/lock-protocol-limit" instead.

    Returns a list of protocols of all locks in the access control system.

    Performs: GET /v1/lock-protocol

    Parameters:
    offset   -- (query) Offset for paging

    limit    -- (query) Limit of result size

    area_id  -- (query:areaId) Filter protocols by area id

    lock_id  -- (query:lockId) Filter protocols by lock id

    from_ts  -- (query:from) Timestamp from when the protocols need to be considered
                (ISO 8601-format compliant date with time in UTC, milliseconds
                precision)

    to_ts    -- (query:to) Timestamp until when the protocols need to be considered
                (ISO 8601-format compliant date with time in UTC, milliseconds
                precision)

    language -- (query) Language codes as a comma-separated list of IETF (bcp47)
                language tags (e.g. de-DE, en-UK) or "all" for all possible
                languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/lock-protocol"

    query = {
        "offset": offset,
        "limit": limit,
        "areaId": area_id,
        "lockId": lock_id,
        "from": from_ts,
        "to": to_ts,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_lock_protocol_limited(offset=None, limit=None, area_id=None, lock_id=None, from_ts=None, to_ts=None, language='de-DE'):
    """
    Gets protocol of locks.

    Returns a list of protocol entries of all locks in the access control system. If
    'from' and 'to' is missing, a default period of 'one day' is used. The period
    between 'from' and 'to' can be maximum one year (365 days).

    Performs: GET /v1/lock-protocol-limit

    Parameters:
    offset   -- (query) Offset for paging

    limit    -- (query) Limit of result size

    area_id  -- (query:areaId) Filter protocols by area id

    lock_id  -- (query:lockId) Filter protocols by lock id

    from_ts  -- (query:from) Timestamp from when the protocol entries need to be
                considered (inclusive, ISO 8601-format compliant date with time in
                UTC, milliseconds precision)

    to_ts    -- (query:to) Timestamp until when the protocol entries need to be
                considered (inclusive, ISO 8601-format compliant date with time in
                UTC, milliseconds precision)

    language -- (query) Language codes as a comma-separated list of IETF (bcp47)
                language tags (e.g. de-DE, en-UK) or "all" for all possible
                languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/lock-protocol-limit"

    query = {
        "offset": offset,
        "limit": limit,
        "areaId": area_id,
        "lockId": lock_id,
        "from": from_ts,
        "to": to_ts,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_locks(offset=None, limit=None, calendar_id=None, locking_system_id=None):
    """
    Gets information of all locks.

    Returns a list of all locks with their information, sorted by lock id in
    ascending order. Maintenance tasks of a lock can be determined by using the
    maintenance-tasks resource (with lockId as query parameter for a single lock).

    Performs: GET /v1/locks

    Parameters:
    offset            -- (query) Offset for paging

    limit             -- (query) Limit of result size

    calendar_id       -- (query:calendarId) Filter locks by holiday calendar id

    locking_system_id -- (query:lockingSystemId) Filter locks by technical
                         identifier lockingSystemId

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks"

    query = {
        "offset": offset,
        "limit": limit,
        "calendarId": calendar_id,
        "lockingSystemId": locking_system_id,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def add_shared_lock(body):
    """
    Redeems a sharing code to add a lock from another access control system.

    Returns the shared lock with its information. The following global sharing codes
    are available in the integration environment: AaBbCcDdEe11, AaBbCcDdEe22,
    AaBbCcDdEe33

    Performs: POST /v1/locks/add-shared-lock

    Parameters:
    body -- (body) Data to redeem sharing code

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Sharing code not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/add-shared-lock"

    return Request("POST", path, json=body)


def get_lock(lock_id):
    """
    Gets information of a specific lock.

    Returns a specific lock with its information.

    Performs: GET /v1/locks/{lockId}

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}"

    return Request("GET", path)


def update_lock(lock_id, body):
    """
    Updates the provided lock.

    Updates the provided lock and returns the new version of the lock object.

    Performs: PUT /v1/locks/{lockId}

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    body    -- (body) Lock to be updated

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied, deserialization or validation
          errors)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (409) Lock updated by another client in the meantime
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}"

    return Request("PUT", path, json=body)


def unmark_lock_as_to_be_removed(lock_id):
    """
    Aborts removal of a lock (removes the to be removed mark on the lock)

    Returns the lock whose removal was aborted.

    Performs: POST /v1/locks/{lockId}/abort-remove

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. not marked as to be removed)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/abort-remove"

    return Request("POST", path)


def mark_lock_as_to_be_removed(lock_id):
    """
    Marks a lock as to be removed. Lock needs to be synchronized to be actually
    removed.

    Returns the lock that has been marked as to be removed.

    Performs: POST /v1/locks/{lockId}/remove

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. already marked as to be removed)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/remove"

    return Request("POST", path)


def get_lock_settings(lock_id):
    """
    Gets settings of a specific lock.

    Returns settings of a specific lock.

    Performs: GET /v1/locks/{lockId}/settings

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings"

    return Request("GET", path)


def update_lock_settings(lock_id, body):
    """
    Updates settings of the lock.

    Updates lock settings and returns the new settings of the lock.

    Performs: PUT /v1/locks/{lockId}/settings

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    body    -- (body) Lock settings to be updated

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings"

    return Request("PUT", path, json=body)


def get_active_shares(lock_id):
    """
    Returns a list of other access control systems your lock has been shared with.



    Performs: GET /v1/locks/{lockId}/settings/active-shares

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/active-shares"

    return Request("GET", path)


def remove_active_shares(lock_id, body):
    """
    Removes shares for a specific lock.

    Returns a list of just removed shares where the lock needs to be synchronized.

    Performs: POST /v1/locks/{lockId}/settings/active-shares/remove

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    body    -- (body) A list of customerNumber

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/active-shares/remove"

    return Request("POST", path, json=body)


def get_assigned_areas(lock_id):
    """
    Gets assigned areas of a specific lock.



    Performs: GET /v1/locks/{lockId}/settings/assigned-areas

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/assigned-areas"

    return Request("GET", path)


def assign_areas(lock_id, body):
    """
    Assigns areas to the specific lock.

    Returns a list of the just assigned areas.

    Performs: POST /v1/locks/{lockId}/settings/assigned-areas/add

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    body    -- (body) A list of areaIds

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/assigned-areas/add"

    return Request("POST", path, json=body)


def unassign_areas(lock_id, body):
    """
    Unassigns areas from the specific lock.

    Returns a list of just unassigned areas where the lock needs to be synchronized.

    Performs: POST /v1/locks/{lockId}/settings/assigned-areas/remove

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    body    -- (body) A list of areaIds

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/assigned-areas/remove"

    return Request("POST", path, json=body)


def get_sharing_codes(lock_id):
    """
    Returns a list of sharing codes for a specific lock.



    Performs: GET /v1/locks/{lockId}/settings/sharing-codes

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/sharing-codes"

    return Request("GET", path)


def create_sharing_code(lock_id):
    """
    Creates sharing code for a specific lock.

    Returns the created sharing code.

    Performs: POST /v1/locks/{lockId}/settings/sharing-codes

    Parameters:
    lock_id -- (path:lockId) Unique identifier of the lock

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/sharing-codes"

    return Request("POST", path)


def delete_sharing_code(lock_id, sharing_code_id):
    """
    Removes sharing code from the specific lock.

    Returns id of the deleted SharingCode.

    Performs: DELETE /v1/locks/{lockId}/settings/sharing-codes/{sharingCodeId}

    Parameters:
    lock_id         -- (path:lockId) Unique identifier of the lock

    sharing_code_id -- (path:sharingCodeId) Unique identifier of the sharing code

    Response:
    (200) successful operation
    (400) Bad request (e.g. invalid ID supplied)
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Forbidden, only allowed for lock owner
    (404) Lock not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/locks/{lock_id}/settings/sharing-codes/{sharing_code_id}"

    return Request("DELETE", path)


def get_maintenance_tasks(lock_id=None, lock_identifier=None, door_name=None, alternative_door_name=None, offset=None, limit=None):
    """
    Gets all maintenance tasks.

    Returns a list of all available maintenance tasks of the access control system,
    sorted by lockId in ascending order.

    Performs: GET /v1/maintenance-tasks

    Parameters:
    lock_id               -- (query:lockId) Filter maintenance tasks by lock id

    lock_identifier       -- (query:lockIdentifier) Filter maintenance tasks by lock
                             identifier

    door_name             -- (query:doorName) Filter maintenance tasks by door name

    alternative_door_name -- (query:alternativeDoorName) Filter maintenance tasks by
                             alternative door name

    offset                -- (query) Offset for paging

    limit                 -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/maintenance-tasks"

    query = {
        "lockId": lock_id,
        "lockIdentifier": lock_identifier,
        "doorName": door_name,
        "alternativeDoorName": alternative_door_name,
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_media(person_id=None, locking_system_id=None, assignment_status=None, offset=None, limit=None):
    """
    Gets information of all media.

    Returns a list of all media defined in the access control system, sorted by
    medium id in ascending order.

    Performs: GET /v1/media

    Parameters:
    person_id         -- (query:personId) Filter media by person id

    locking_system_id -- (query:lockingSystemId) Filter media by technical
                         identifier lockingSystemId

    assignment_status -- (query:assignmentStatus) Filter media by assignment status

    offset            -- (query) Offset for paging

    limit             -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media"

    query = {
        "personId": person_id,
        "lockingSystemId": locking_system_id,
        "assignmentStatus": assignment_status,
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def assign_owner_to_medium(body):
    """
    Assigns a person to a medium for each provided assignment.

    Creates a person assignment for a medium according to the provided list of
    assignments and returns the resulting assignment list.

    Performs: POST /v1/media/assign

    Parameters:
    body -- (body) List of medium assignments

    Response:
    (200) successful operation
    (400) Bad request (syntactically wrong / semantically wrong / cannot be
          fulfilled for other reasons, e.g., other business rules like the medium
          still has authorizations)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium or person not found
    (409) Medium already assigned
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/assign"

    return Request("POST", path, json=body)


def cancel_medium_assignments(body):
    """
    Cancels assignments of media.

    Cancels the person assignments of the provided list of media and returns a list
    of identifiers of the updated medium objects.

    Performs: POST /v1/media/cancel-assignment

    Parameters:
    body -- (body) List of unique medium identifiers

    Response:
    (200) successful operation
    (400) Bad request (syntactically wrong / semantically wrong / cannot be
          fulfilled for other reasons, e.g., other business rules like the medium
          still has authorizations)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/cancel-assignment"

    return Request("POST", path, json=body)


def get_cards(person_id=None, locking_system_id=None, assignment_status=None, offset=None, limit=None):
    """
    Gets information of all cards.

    Returns a list of all media of type 'card' defined in the access control system.

    Performs: GET /v1/media/cards

    Parameters:
    person_id         -- (query:personId) Filter cards by person id

    locking_system_id -- (query:lockingSystemId) Filter cards by technical
                         identifier lockingSystemId

    assignment_status -- (query:assignmentStatus) Filter cards by assignment status

    offset            -- (query) Offset for paging

    limit             -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/cards"

    query = {
        "personId": person_id,
        "lockingSystemId": locking_system_id,
        "assignmentStatus": assignment_status,
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def update_cards(body):
    """
    Updates list of cards.

    Updates the provided list of cards and returns a list of new object versions.

    Performs: PUT /v1/media/cards

    Parameters:
    body -- (body) List of cards to be updated

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Card not found
    (409) Conflict - medium has been changed
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/cards"

    return Request("PUT", path, json=body)


def get_card(card_id):
    """
    Gets information of specific card.

    Returns all information of provided medium of type 'card'.

    Performs: GET /v1/media/cards/{cardId}

    Parameters:
    card_id -- (path:cardId) Unique identifier of the card

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/cards/{card_id}"

    return Request("GET", path)


def get_phones(person_id=None, locking_system_id=None, assignment_status=None, phone_number=None, offset=None, limit=None):
    """
    Gets information of all phones.

    Returns a list of all media of type 'phone' defined in the access control
    system.

    Performs: GET /v1/media/phones

    Parameters:
    person_id         -- (query:personId) Filter phones by person id

    locking_system_id -- (query:lockingSystemId) Filter phones by technical
                         identifier lockingSystemId

    assignment_status -- (query:assignmentStatus) Filter phones by assignment status

    phone_number      -- (query:phoneNumber) Filter phones by phone number

    offset            -- (query) Offset for paging

    limit             -- (query) Limit of result size

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones"

    query = {
        "personId": person_id,
        "lockingSystemId": locking_system_id,
        "assignmentStatus": assignment_status,
        "phoneNumber": phone_number,
        "offset": offset,
        "limit": limit,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def create_phones(body):
    """
    Adds list of new phones.

    Creates and adds the provided phones to the access control system and returns a
    list of the new phone objects. Please check before if a phone already exists
    with the given phone number to prevent duplicates.

    Performs: POST /v1/media/phones

    Parameters:
    body -- (body) List of phones to be added

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (409) Phone already exists
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones"

    return Request("POST", path, json=body)


def update_phones(body):
    """
    Updates list of phones.

    Updates the provided list of phones and returns a list of new object versions.
    Please check before if a phone already exists with the given phone number to
    prevent duplicates.

    Performs: PUT /v1/media/phones

    Parameters:
    body -- (body) List of phones to be updated

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Phone not found
    (409) Conflict - medium has been changed
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones"

    return Request("PUT", path, json=body)


def delete_phones(body):
    """
    Deletes provided phones.

    Deletes the provided phones and returns a list of identifiers of all deleted
    objects.

    Performs: DELETE /v1/media/phones

    Parameters:
    body -- (body) List of unique identifiers of all phones to be deleted

    Response:
    (200) successful operation
    (400) Bad request (e.g. wrong data type supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Phone not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones"

    return Request("DELETE", path, json=body)


def get_phone(phone_id):
    """
    Gets information of specific phone.

    Returns all information of provided medium of type 'phone'.

    Performs: GET /v1/media/phones/{phoneId}

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}"

    return Request("GET", path)


def generate_pairing_code_for_phone(phone_id):
    """
    Generates a new pairing code for a phone.

    Generates a new pairing code for the provided phone and returns a new version of
    the phone object.

    Performs: POST /v1/media/phones/{phoneId}/pairing

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Phone not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}/pairing"

    return Request("POST", path)


def reset_pin_of_phone(phone_id):
    """
    Resets PIN of the phone.

    Resets the PIN of the provided phone and returns new version of the phone object
    with set PIN reset time. After the phone was synchronized the PIN flag is reset.

    Performs: POST /v1/media/phones/{phoneId}/pin-reset

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone to reset the PIN

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Phone not found
    (409) No PIN set for phone
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}/pin-reset"

    return Request("POST", path)


def send_registration_code_to_phone_1(phone_id):
    """
    Deprecated/Legacy: This resource will be removed in future versions. Please use
    resource "/v1/media/phones/{phoneId}/send-registration-code/sms" instead.

    Sends a generated pairing code per SMS to the phone and returns a new version of
    the phone object.

    Performs: POST /v1/media/phones/{phoneId}/send-registration-code

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The SMS limit has been exceeded
    (404) Phone not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}/send-registration-code"

    return Request("POST", path)


def send_registration_code_to_phone(phone_id, body=None):
    """
    Deprecated/Legacy: This resource will be removed in future versions. Please use
    resource "/v1/media/phones/{phoneId}/send-registration-code/sms" instead.

    Sends a generated pairing code per SMS to the phone and returns a new version of
    the phone object.

    Performs: POST /v1/media/phones/{phoneId}/send-registration-code-with-parameters

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone

    body     -- (body) Send registration code request wrapper

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The SMS limit has been exceeded
    (404) Phone not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}/send-registration-code-with-parameters"

    return Request("POST", path, json=body)


def send_registration_code_to_phone_via_mail(phone_id, body):
    """
    Sends a pairing code while the email subject and text to be sent can be
    configured.

    Sends a generated pairing code per email and returns a new version of the phone
    object.

    Performs: POST /v1/media/phones/{phoneId}/send-registration-code/mail

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone

    body     -- (body) Send registration code via email request wrapper

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The email limit has been exceeded
    (404) Phone not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}/send-registration-code/mail"

    return Request("POST", path, json=body)


def send_registration_code_to_phone_via_sms(phone_id, body):
    """
    Sends pairing code to phone while the SMS text to be sent can be configured.

    Sends a generated pairing code per SMS to the phone and returns a new version of
    the phone object.

    Performs: POST /v1/media/phones/{phoneId}/send-registration-code/sms

    Parameters:
    phone_id -- (path:phoneId) Unique identifier of the phone

    body     -- (body) Send registration code request wrapper

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The SMS limit has been exceeded
    (404) Phone not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/phones/{phone_id}/send-registration-code/sms"

    return Request("POST", path, json=body)


def get_medium(medium_id):
    """
    Gets information of a specific medium.

    Returns all information of a specific medium defined in the access control
    system.

    Performs: GET /v1/media/{mediumId}

    Parameters:
    medium_id -- (path:mediumId) Unique identifier of the medium

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/{medium_id}"

    return Request("GET", path)


def deactivate_medium(medium_id, reason, comment=None):
    """
    Deactivates provided medium.

    Deactivates the provided medium and returns a new version of the medium object.
    The fields "reason" and "comment" are saved in the system protocol and are not
    part of the response.

    Performs: POST /v1/media/{mediumId}/deactivate

    Parameters:
    medium_id -- (path:mediumId) Unique identifier of the medium to be deactivated

    reason    -- (query) Reason of deactivation (user defined input that can be used
                 to describe the reasons for deactivating a medium, e.g. has been
                 lost / was stolen / is broken)

    comment   -- (query) Additional comment of deactivation (user defined input that
                 can be used to add further details regarding the reason for
                 deactivating a medium, e.g. when all details won't fit within the
                 reason field)

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/{medium_id}/deactivate"

    query = {
        "reason": reason,
        "comment": comment,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("POST", path, params=params)


def empty_medium(medium_id):
    """
    Empties provided medium.

    Empties the provided medium and returns a new version of the medium object. All
    authorizations will be deleted from the medium. The person assignment of the
    medium does not get cancelled.

    Performs: POST /v1/media/{mediumId}/empty

    Parameters:
    medium_id -- (path:mediumId) Unique identifier of the medium

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/{medium_id}/empty"

    return Request("POST", path)


def reactivate_medium(medium_id, reason, recover_authorizations, comment=None):
    """
    Reactivates provided medium.

    Reactivates the provided medium and returns a new version of the medium object.
    The fields "reason" and "comment" are saved in the system protocol and are not
    part of the response.

    Performs: POST /v1/media/{mediumId}/reactivate

    Parameters:
    medium_id              -- (path:mediumId) Unique identifier of the medium to be
                              reactivated

    reason                 -- (query) Reason of reactivation (user defined input
                              that can be used to describe the reasons for
                              reactivating a medium, e.g. a medium has been found
                              again)

    comment                -- (query) Additional comment of reactivation (user
                              defined input that can be used to add further details
                              regarding the reason for reactivating a medium, e.g.
                              when all details won't fit within the reason field)

    recover_authorizations -- (query:recoverAuthorizations) Recover authorizations
                              available prior to deactivation

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Medium not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/media/{medium_id}/reactivate"

    query = {
        "reason": reason,
        "comment": comment,
        "recoverAuthorizations": recover_authorizations,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("POST", path, params=params)


def get_medium_protocol(offset=None, limit=None, from_ts=None, to_ts=None, medium_id=None, language='de-DE'):
    """
    Deprecated/Legacy: This resource will be removed in future versions. Please use
    resource "/v1/medium-protocol-limit" instead.

    Returns a list of protocol of media in the access control system.

    Performs: GET /v1/medium-protocol

    Parameters:
    offset    -- (query) Offset for paging

    limit     -- (query) Limit of result size

    from_ts   -- (query:from) Timestamp from when the protocols need to be
                 considered (ISO 8601-format compliant date with time in UTC,
                 milliseconds precision)

    to_ts     -- (query:to) Timestamp until when the protocol need to be considered
                 (ISO 8601-format compliant date with time in UTC, milliseconds
                 precision)

    medium_id -- (query:mediumId) Filter authorizations by medium id

    language  -- (query) Language codes as a comma-separated list of IETF (bcp47)
                 language tags (e.g. de-DE, en-UK) or "all" for all possible
                 languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/medium-protocol"

    query = {
        "offset": offset,
        "limit": limit,
        "from": from_ts,
        "to": to_ts,
        "mediumId": medium_id,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_medium_protocol_limited(offset=None, limit=None, from_ts=None, to_ts=None, medium_id=None, language='de-DE'):
    """
    Gets protocol of media.

    Returns a list of protocol entries of media in the access control system. If
    'from' and 'to' is missing, a default period of 'one day' is used. The period
    between 'from' and 'to' can be maximum one year (365 days).

    Performs: GET /v1/medium-protocol-limit

    Parameters:
    offset    -- (query) Offset for paging

    limit     -- (query) Limit of result size

    from_ts   -- (query:from) Timestamp from when the protocol entries need to be
                 considered (inclusive, ISO 8601-format compliant date with time in
                 UTC, milliseconds precision)

    to_ts     -- (query:to) Timestamp until when the protocol entries need to be
                 considered (inclusive, ISO 8601-format compliant date with time in
                 UTC, milliseconds precision)

    medium_id -- (query:mediumId) Filter authorizations by medium id

    language  -- (query) Language codes as a comma-separated list of IETF (bcp47)
                 language tags (e.g. de-DE, en-UK) or "all" for all possible
                 languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/medium-protocol-limit"

    query = {
        "offset": offset,
        "limit": limit,
        "from": from_ts,
        "to": to_ts,
        "mediumId": medium_id,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_pending_phone_replacements():
    """
    Gets all pending phone replacements.

    Returns a list of all pending phone replacements sorted by creation date
    ascending.

    Performs: GET /v1/pending-phone-replacements

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/pending-phone-replacements"

    return Request("GET", path)


def approve_pending_phone_replacement(replacement_id):
    """
    Approves pending phone replacement



    Performs: POST /v1/pending-phone-replacements/{replacementId}/approve

    Parameters:
    replacement_id -- (path:replacementId) Unique identifier of the replacement
                      operation

    Response:
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (403) Approval not possible due to replacement operation state or not enough
          credits
    (404) Replacement operation not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/pending-phone-replacements/{replacement_id}/approve"

    return Request("POST", path)


def reject_pending_phone_replacement(replacement_id):
    """
    Rejects pending phone replacement



    Performs: POST /v1/pending-phone-replacements/{replacementId}/reject

    Parameters:
    replacement_id -- (path:replacementId) Unique identifier of the replacement
                      operation

    Response:
    (401) Unauthorized (e.g. API key not found, not allowed due to IP whitelist)
    (404) Replacement operation not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/pending-phone-replacements/{replacement_id}/reject"

    return Request("POST", path)


def get_persons(offset=None, limit=None, first_name=None, last_name=None, secondary_identification=None, search=None):
    """
    Gets all persons.

    Returns a list of all persons defined in the access control system, sorted by
    person id in ascending order.

    Performs: GET /v1/persons

    Parameters:
    offset                   -- (query) Offset for paging

    limit                    -- (query) Limit of result size

    first_name               -- (query:firstName) Filter persons by first name

    last_name                -- (query:lastName) Filter persons by last name

    secondary_identification -- (query:secondaryIdentification) Filter persons by
                                secondary identification

    search                   -- (query) Filter persons by matches in: first name,
                                last name, secondary identification, email address,
                                comment, street, city, country

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/persons"

    query = {
        "offset": offset,
        "limit": limit,
        "firstName": first_name,
        "lastName": last_name,
        "secondaryIdentification": secondary_identification,
        "search": search,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def create_persons(body):
    """
    Adds list of new persons.

    Creates and adds the provided persons to the access control system and returns a
    list of the new person objects.

    Performs: POST /v1/persons

    Parameters:
    body -- (body) List of persons to be added

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/persons"

    return Request("POST", path, json=body)


def update_persons(body):
    """
    Updates list of persons.

    Updates the provided list of persons and returns a list of new object versions.

    Performs: PUT /v1/persons

    Parameters:
    body -- (body) List of persons to be updated

    Response:
    (200) successful operation
    (400) Bad request (e.g., unknown attribute supplied, required attribute is
          missing, length or unique constraint violated)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Person not found
    (409) Conflict - person has been changed
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/persons"

    return Request("PUT", path, json=body)


def delete_persons(body):
    """
    Deletes provided persons.

    Deletes the provided persons and returns a list of identifiers of all deleted
    objects.

    Performs: DELETE /v1/persons

    Parameters:
    body -- (body) List of unique identifiers of all persons to be deleted

    Response:
    (200) successful operation
    (400) Bad request (e.g., wrong data type supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Person not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/persons"

    return Request("DELETE", path, json=body)


def get_person(person_id):
    """
    Gets a specific person.

    Returns a specific person defined in the access control system.

    Performs: GET /v1/persons/{personId}

    Parameters:
    person_id -- (path:personId) Unique identifier of the person

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid ID supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Person not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/persons/{person_id}"

    return Request("GET", path)


def reset_test_data():
    """
    Resets test data in the integration environment.

    Resets the test data for the customer generated in the integration environment.

    Performs: POST /v1/public-mgmt/reset-test-data

    Parameters:
    None

    Response:
    (204) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (404) Customer data not found
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/public-mgmt/reset-test-data"

    return Request("POST", path)


def send_a_key(body):
    """
    Deprecated/Legacy: This resource will be removed in future versions. Please use
    resource "/v1/send-a-key/sms" instead.

    Based on the given phone number this request sends a registration link via SMS
    for easy installation of the AirKey app. It simplifies the task of creating new
    mobile app users by implicitly creating new persons, phones and authorizations
    of type 'SIMPLE' if needed, i.e. it reuses an existing person if found. Please
    check before if a phone already exists with the given phone number to prevent
    duplicates (GET /media/phones using the filter phoneNumber). The reason why
    duplicates are allowed is to be able to create a new phone with an already
    existing phone number so it is not mandatory to delete an old phone before
    creating the new phone with the same phone number.
    Authorization creation mirrors the behaviour of POST /authorizations/simple. If
    you need more control consider creating a phone and person with this call and
    using the advanced authorization interface for creating authorizations.
    Either lockId or areaId needs to be set for an authorization. It's not possible
    to set both IDs at the same time.

    Performs: POST /v1/send-a-key

    Parameters:
    body -- (body) Send-A-Key via SMS request wrapper

    Response:
    (200) successful operation
    (400) Bad request (e.g., wrong data type supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The SMS limit has been exceeded
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/send-a-key"

    return Request("POST", path, json=body)


def send_a_key_via_mail(body):
    """
    Sends a registration code via email and creates all necessary prerequisites if
    needed.

    This request sends a registration link via email for easy installation of the
    AirKey app. If the request contains an email address, it will be updated for the
    person.It simplifies the task of creating new mobile app users by implicitly
    creating new persons, phones and authorizations of type 'SIMPLE' if needed, i.e.
    it reuses an existing person if found. Please check before if a phone already
    exists with the given phone number to prevent duplicates (GET /media/phones
    using the filter phoneNumber). The reason why duplicates are allowed is to be
    able to create a new phone with an already existing phone number so it is not
    mandatory to delete an old phone before creating the new phone with the same
    phone number.
    Authorization creation mirrors the behaviour of POST /authorizations/simple. If
    you need more control consider creating a phone and person with this call and
    using the advanced authorization interface for creating authorizations.
    Either lockId or areaId needs to be set for an authorization. It's not possible
    to set both IDs at the same time.

    Performs: POST /v1/send-a-key/mail

    Parameters:
    body -- (body) Send-A-Key via email request wrapper

    Response:
    (200) successful operation
    (400) Bad request (e.g., wrong data type supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The email limit has been exceeded
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/send-a-key/mail"

    return Request("POST", path, json=body)


def send_a_key_via_sms(body):
    """
    Sends a registration code to the phone and creates all necessary prerequisites
    if needed.

    Based on the given phone number this request sends a registration link via SMS
    for easy installation of the AirKey app. It simplifies the task of creating new
    mobile app users by implicitly creating new persons, phones and authorizations
    of type 'SIMPLE' if needed, i.e. it reuses an existing person if found. Please
    check before if a phone already exists with the given phone number to prevent
    duplicates (GET /media/phones using the filter phoneNumber). The reason why
    duplicates are allowed is to be able to create a new phone with an already
    existing phone number so it is not mandatory to delete an old phone before
    creating the new phone with the same phone number.
    Authorization creation mirrors the behaviour of POST /authorizations/simple. If
    you need more control consider creating a phone and person with this call and
    using the advanced authorization interface for creating authorizations.
    Either lockId or areaId needs to be set for an authorization. It's not possible
    to set both IDs at the same time.

    Performs: POST /v1/send-a-key/sms

    Parameters:
    body -- (body) Send-A-Key via SMS request wrapper

    Response:
    (200) successful operation
    (400) Bad request (e.g., wrong data type supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (403) The SMS limit has been exceeded
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/send-a-key/sms"

    return Request("POST", path, json=body)


def get_customer_settings():
    """
    Gets settings details.

    Returns stored settings of the customer.

    Performs: GET /v1/settings

    Parameters:
    None

    Response:
    (200) successful operation
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/settings"

    return Request("GET", path)


def get_system_protocol(offset=None, limit=None, id=None, lock_id=None, medium_id=None, event=None, user_id=None, administrator=None, from_ts=None, to_ts=None, language='de-DE'):
    """
    Deprecated/Legacy: This resource will be removed in future versions. Please use
    resource "/v1/system-protocol-limit" instead.

    Returns the system protocol with all events that were conducted by the
    administrators of the access control system.

    Performs: GET /v1/system-protocol

    Parameters:
    offset        -- (query) Offset for paging

    limit         -- (query) Limit of result size

    id            -- (query) Filter events by unique protocol entry identifier

    lock_id       -- (query:lockId) Filter events by unique lock id

    medium_id     -- (query:mediumId) Filter events by unique medium id

    event         -- (query) Filter events by event type

    user_id       -- (query:userId) Filter events by unique administrator user
                     identifier

    administrator -- (query) Filter events by name of administrator

    from_ts       -- (query:from) Timestamp from when the protocols need to be
                     considered (ISO 8601-format compliant date with time in UTC,
                     milliseconds precision: yyyy-mm-ddThh:mm:ss.SSSZ)

    to_ts         -- (query:to) Timestamp until when the protocol need to be
                     considered (ISO 8601-format compliant date with time in UTC,
                     milliseconds precision: yyyy-mm-ddThh:mm:ss.SSSZ)

    language      -- (query) Language codes as a comma-separated list of IETF
                     (bcp47) language tags (e.g. de-DE, en-UK) or "all" for all
                     possible languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/system-protocol"

    query = {
        "offset": offset,
        "limit": limit,
        "id": id,
        "lockId": lock_id,
        "mediumId": medium_id,
        "event": event,
        "userId": user_id,
        "administrator": administrator,
        "from": from_ts,
        "to": to_ts,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


def get_system_protocol_limited(offset=None, limit=None, id=None, lock_id=None, medium_id=None, event=None, user_id=None, administrator=None, from_ts=None, to_ts=None, language='de-DE'):
    """
    Gets system protocol.

    Returns the system protocol with events that were conducted by the
    administrators of the access control system. If 'from' and 'to' is missing, a
    default period of 'one day' is used. The period between 'from' and 'to' can be
    maximum one year (365 days).

    Performs: GET /v1/system-protocol-limit

    Parameters:
    offset        -- (query) Offset for paging

    limit         -- (query) Limit of result size

    id            -- (query) Filter events by unique protocol entry identifier

    lock_id       -- (query:lockId) Filter events by unique lock id

    medium_id     -- (query:mediumId) Filter events by unique medium id

    event         -- (query) Filter events by event type

    user_id       -- (query:userId) Filter events by unique administrator user
                     identifier

    administrator -- (query) Filter events by name of administrator

    from_ts       -- (query:from) Timestamp from when the protocol entries need to
                     be considered (inclusive, ISO 8601-format compliant date with
                     time in UTC, milliseconds precision: yyyy-mm-ddThh:mm:ss.SSSZ)

    to_ts         -- (query:to) Timestamp until when the protocol entries need to be
                     considered (inclusive, ISO 8601-format compliant date with time
                     in UTC, milliseconds precision: yyyy-mm-ddThh:mm:ss.SSSZ)

    language      -- (query) Language codes as a comma-separated list of IETF
                     (bcp47) language tags (e.g. de-DE, en-UK) or "all" for all
                     possible languages used for translations

    Response:
    (200) successful operation
    (400) Bad request (e.g., invalid filter or paging parameters supplied)
    (401) Unauthorized (e.g., API key not found, not allowed due to IP whitelist)
    (429) Too many requests - daily request limit exceeded
    (500) Internal server error
    (503) Service unavailable
    """
    path = f"/v1/system-protocol-limit"

    query = {
        "offset": offset,
        "limit": limit,
        "id": id,
        "lockId": lock_id,
        "mediumId": medium_id,
        "event": event,
        "userId": user_id,
        "administrator": administrator,
        "from": from_ts,
        "to": to_ts,
        "language": language,
    }
    params = {key: value
              for key, value in query.items()
              if key is not None}

    return Request("GET", path, params=params)


__all__ = [name
           for name in globals().keys()
           if not name.startswith("_")]
