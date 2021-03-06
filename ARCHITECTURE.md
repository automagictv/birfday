# Requirements

 * Store data about friends/family birthday's.
 * Read data about birthdays.
 * Understand if today is a birthday (or multiple bdays).
 * Handle leap year birthdays.
 * Add / Remove / Update birthday/person data.
 * Integrate with some notification / messaging API.
 * Can send messages to me via that API.
 * All implementations must be testable.

# Data Model

 * DB Models
    * Birthday
        * first name
        * last name
        * month
        * day
        * note
        * dt_created
        * dt_updated
 * Messaging / API Helper
    * Create client / connect to api
    * Send message
 * Config
    * Constants
 * Runner
    * Db connection objects
    * Main function

# Happy Path

 1. Spin up, read config and instantiate logger.
 2. Read database to get birthdays.
 3. See if today is a birthday.
 4. For all birthdays today, notify me and include template message.
 5. Exit.

# Expansion

 * Add a gift tracker / recommender that reminds us to buy gifts.
 * Expand to different event types (anniversaries, graduation, etc.)
 * Add CLI functionality to interact with db / update data one by one.
 * Store sample / default messages so you can copy/paste.
 * If your friends are on telegram you may even be able to fully automate this.
