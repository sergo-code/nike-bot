# Nike Bot
You can send the bot a link to the product you like, choose the size and subscribe. 
If the price drops and your size is available, the bot will notify you about it. 
The bot will also notify if your size runs out.  

Example: [@nike_sale_bot](https://t.me/nike_sale_bot)

### Installation
Rename
```
mv .env_pub .env
```

Database: install PostgreSQL

Dependencies
```
python3 -m pip install -r requirements.txt
```

Creating tables in a database
```
python3 db/db.py
```

### Usage
```
python3 bot.py
```
### Admin Tools
Available admin_tg from .env
- Button "🔔 User Information"
- /user <telegram_id> (information about subscriptions of the specified user)
- /limit <telegram_id> <max_count> (set the maximum subscription limit for the specified user)
