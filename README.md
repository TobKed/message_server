# messages server
> CLI apps to managae users and send messages between them

## Requirements

* The environmental variable with database URI shall be set
    ```
    # Example: 
    SERVER_DB_URI = "postgresql://user:secret@localhost/mydb"
    ```

* Models module contains several methods to set up database
    ```
    nuke_db()
    create_db()
    create_users_table()
    create_messages_table()
    ```

### Users

List of all arguments
```
'-u', '--username', help='user login'
'-p', '--password', help='user password'
'-l', '--list', action='store_true', help='list all users'
'-d', '--delete', action='store_true', help='delete user'
'-n', '--new-pass', help='new user password'
'-e', '--edit', help='edit user login'
'-c', '--confirm', help='confirm password for new created user
                         or confirm new password for existing user
                         or confirm new login``
                         or confirm login for deleted user'
```

#### Usage examples

* List of all users
    ```             
    python3 users.py --list
    python3 users.py -l
    ```

* Edit user login
    ```
    python3 users.py --username LOGIN --password PASSWORD --edit NEW_LOGIN --confirm NEW_LOGIN
    python3 users.py -u LOGIN -p PASSWORD -e NEW_LOGIN -c NEW_LOGIN
    ```

* New user password
    ```
    python3 users.py --username LOGIN --password PASSWORD --new-pass NEW_PASSWORD --confirm NEW_PASSWORD
    python3 users.py -u LOGIN -p PASSWORD -n NEW_PASSWORD -c NEW_PASSWORD
    ```

* Delete user
    ```
    python3 users.py --username LOGIN --password PASSWORD --delete --confirm LOGIN
    python3 users.py -u LOGIN -p PASSWORD -d -c LOGIN
    ```


### Messages                                                                
                                                                         
List of all arguments                                                    
```
'-u', '--username', help='user login'
'-p', '--password', help='user password'
'-l', '--list', help='list all messages or list of all mesages for given user'
'-s', '--send', nargs="+", help='message text'
'-t', '--to', help='recipient login'
```

#### Usage examples                                                      
                                                                         
* List of all messages                                                     
    ```                                                                  
    python3 users.py --list                                              
    python3 users.py -l                                                  
    ```