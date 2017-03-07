# Urban Robot Advanced Chat System (URACS)
This is a KTN (TTM4100) group project at NTNU

We strive to deliver a fast, efficient, and lightweight chat system for the world to enjoy. Our interface will be entirely command line based.

Rendering command lines don't require much computer power, so URACS will consume much less energy on the client's computer compared to other chat applications. Therefore, URACS is contributing to the global project of not surpassing the UN two-degree goal.

## Structure

### 1. Server
The server will be built to specs according to the assignment. If we have some time to kill in the end, we would like to implement some extra features.

#### Requests

- `login <username>`
    - Required in task. Username and ip stored in `active-users`.
- `logout`
    - Removes user from `active-users`.
- `help`
    - Some nifty help will be shown in the client.
- `history`
    - History stored in list containing `user` and `message`.
- `msg <message>`
    - Posts a message.
- `names`
    - Lists all usernames from `active-users`.

### 2. Client
The client will format the messages in plain, but efficient way. If we have some extra time, we may implement basic formatting (stealing syntax from Markdown).

#### Chat format 

```text
   Urban Robot Advanced Chat System
   --------------------------------
07.03.17 17.33: y0l0_p3t3r joined.
07.03.17 17.34: y0l0_p3t3r:
    Hey guys, how's it hangin?
07.03.17 17.36: fitn3ss_john:
    Not much, just about to head to the gym
07.03.17 17.36: fitn3ss_john left.
07.03.17 17.36: m4d_b3nny:
    Any of you guys wanna play some Mario Party later 2nite?
07.03.17 17.36: y0l0_p3t3r:
    Nah, I'm good
07.03.17 23:35: fitn3ss_john joined.
07.03.17 23.36: fitn3ss_john:
    I'm in.
```


## Stretch goals
These are some features we would like to implement if we have some time to kill.

- [ ] `login <username> <room_id>`
    - Login to a specific chat room/channel
- [ ] `group <room_id>`
    - Switch to another room.
- [ ] ```msg Hey _guys_, would **you** like to play ***some*** `games`?``` 
    - Formatting, would render to look like this:   
    Hey _guys_, would **you** like to play ***some*** `games`?
- [ ] `login <username> <room_id> <room_pwd>`
    - Logging in to a restricted room.
    