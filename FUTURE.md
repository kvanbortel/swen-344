# Future Plan


## Popularity Tiers

Books now have *popularity tiers*. more popular books may have earlier due dates and late fees may be higher.

### Implementation:

#### Tables:
- *Books:* Add a new column, **`tier_id`**, a foriegn key that maps to the primary key of a new table, *Tiers*.
- *Tiers:*
  - **`id`**: serial key
  - **`days_until_due`**: number of days a book can be checked out without being overdue
  - **`small_fee`**: the fee for a short overdue duration
  - **`large_fee`**: the fee for a longer overdue duration

#### API Changes:
- Add a new function to list books by tier
- Change returnBook API to use new tier values rather than Python constants

## Overdue Warnings

Books that are overdue by a certain amount of time have an automatic warning notification sent out to the user.

### Tables:
- *Users:* Add a new column, **`notification_id`**, a foreign key that maps to the primary key of a new table, *Notifications*.
- *Notifications:* new table
  - **`id`**: serial key
  - **`overdue_warning`**: updates to true when a book is overdue for that user

### API Changes:
- Add a new function to tell a user more information about their overdue warning, including which book it's for and how overdue it is.
- Any time a user tries to interact with the database with the date, a check to the warning system is done with that date as the 'current date'.
