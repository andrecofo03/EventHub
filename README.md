# EventHub

## Description
EventHub is an event management platform that allows activity planning, registration management, and coordination of attendee participation. Organizers can plan events, while attendees can view active events and register for them.

---

## Features

### Attendee
- **Event viewing**: Browse the list of all created events and their details (date, time, location, description).
- **Registration/Cancellation**: Ability to register for an event or cancel registration.
- **Registration management**: Personal page to view all events the user is registered for.
- **User Profile**: Dedicated page to view account details.

### Organizer
- **Event management**: Creation, viewing, editing, and deletion of events (editing/deletion only by the organizer who created the event).
- **Attendee list**: View the list of attendees registered for their events.
- **Event viewing**: Browse all events registered on the platform.
- **User Profile**: Dedicated page to view account details.

### Administrator (Superuser)
- **Control Panel (Django Admin)**: Access to the administration panel to manage events (viewing attendees and deleting events).
- **User Profile**: Dedicated page to view account details.

---

## Database Elements

The database included in the project is located in the **`db.sqlite3`** file (in the project root directory) and contains pre-loaded demo data for immediate testing.

| Role | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin_demo` | `admin12345` |
| **Attendee** | `user_demo` | `user12345` |
| **Organizer** | `manager_demo` | `manager12345` |

I added also two new users from the deployment:

| Role | Username | Password | 
| :--- | :--- | :--- | :--- |
| **Organizer** | `manager_deploy` | `deploy12345` | 
| **Attendee** | `user_deploy` | `deploy12345` | 

---

## Testing scenario

### 1. Login
* Open the browser
* Log in with the **Organizer** account:
 
### 2. Navigate to a Feature
* Once logged in, click on **Create Event** from the options available

### 3. Create and Edit Data
* **Creation**: Fill in the form with the event details required and click **Create**
* **Edit**: Access the details page of the newly created event, click on **Edit**, make a change to one of the fields and confirm

### 4. Test Permissions
* Log in as an **Attendee**:
* **Permission violation test**: Attempt to force navigation by manually entering the event edit URL created earlier in the browser address bar
* **Expected result**: It will prevent access by displaying an error page, because only the organizer that created the event can edit it

### 5. Verify Results
* Return to the main event list
* Click on **Details** of the event created earlier and click **Register**
* Verify that the event appears correctly in your personal **Registrations** page and that the event details show the attendee counter updated correctly  

---

## Deployment Link
https://eventhub-project.vercel.app/