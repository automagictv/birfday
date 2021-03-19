# Requirements

 * Store data about friends/family birthday's.
 * Read data about birthdays.
 * Understand if today is a birthday (or multiple bdays).
 * Add / Remove / Update birthday/person data.
 * Integrate with some notification / messaging API.
 * Can send messages to me via that API.
 * Store sample / default messages so I can just copy/paste.
 * All implementations must be testable.

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
