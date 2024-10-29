![Uploading image.png…]()

Members:
  Bolarde, Miklos Kaiser A.
  Flores, Adrian Ash D. 
  Dela Cerna, Geraldine D.  
Overview:
  1. Purpose and Entities
  This is a Django project likely intended to manage a hospital. The primary entities (models) in the project represent various aspects of this system, such as patients, staff, departments, and billing.
  
  The key models/entities are:
  
    User (Custom): This model is for user authentication and roles. Users can be assigned roles like patient, doctor, or staff. Each role has specific dashboards or permissions.
    
    Patient: Stores information about individual patients, including personal details like name, age, gender, contact info, etc.
    
    Staff: Represents staff members like administrative personnel, nurses, etc. They are categorized by their staff_type.
    
    Department: Represents different departments within the hospital, e.g., Cardiology, Pediatrics. Each department has staff members associated with it.
    
    Doctor: Represents doctors, including their specialization and the type of doctor they are (e.g., surgeon, general practitioner).
    
    Equipment: Represents medical equipment in the hospital, detailing their quantity, type, and price.
    
    Billing: Stores billing information related to patients, including the date, amount, and references to the staff and department involved in the billing process.
    
    Room: Represents patient rooms, including their type and price, and links to a specific department.
    
    Schedule: Represents the schedule of doctors, including the date, time, and associated patient.
Functional Requirement:

    1.	Patient and Doctor Registration and Management 
  	> The system should allow new registration of patients and doctors as well as manage the existing one. This includes taking the basic information like name, age, gender and birthdate. The system also allows users to update and delete records.
  
    2.	User Authentication and Role Management
    > The system should provide user authentication and role-based access control to ensure that only authorised personnel can access specific features and patient information. Roles might include administrators, doctors, nurses, and receptionists.
    
    3.	Doctor’s Dashboard
    > The system should provide a dashboard for doctors, displaying their 
    schedule, patient’s appointment, etc. 
    
    4.	Bed/Room Management
    > The system should allow the hospital to track all bed/room availability,
    indicating whether a bed/room is occupied, vacant, or reserved. This information should be updated in real-time as patients are admitted, transferred, or discharged.
    
    5.	Equipment Usage
    > The system should allow the hospital to monitor, track, and manage
    the usage of equipment.
    
    6.	Billing and Invoice
    > The system should be able to generate bills and invoices for all the
    services the patients provided.
Link to Figma: 
  https://www.figma.com/design/uVoq8MHgWwoexk7hmEdGDu/General-HMS-UX%2FUI?node-id=0-1&t=6nzGkO52hxIJkV2G-1

Link to ERD: 
  https://dbdiagram.io/d/67013d3cfb079c7ebd6f1688
