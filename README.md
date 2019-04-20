### Labs description:

#### McCabe

McCabe metric for Python source code is calculated. Paste your Python source into `textarea` and click on `Calculate McCabe`. You will see code graph and control flow graph below with metric value mentioned in `McCabe: <value>` section

#### SQL Injections

- Using operator `union`. Go to "SQL Injection 1" tab. You will see a list of items in the database, which you can filter with "Search query" input. However, adding to the input query term `' union select first_name from auth_user; --` you can grab users info.
- Verification bypass via boolean operators. Go to "SQL Injection 2" tab. You can login to the system if you enter the right login/password. Database users: `User1 / password`, `root / password`, `User2 / password`. If login succeeded, you will receive a green badge, else it will be read. Entering `') OR 1=1; --` in *password* field along with existing user login or `' OR 1=1; --` in *login* field with any password field will result in your login step completed (you will receive green badge).
- Update records from the url. Go to "SQL Injection 3" tab. You will see a list of items in the database. You can select one and then update its name. If you change url from `/sql3?item=Socks` to `/sql3?item=%27+or+name+%3D+%27Trainers%27%3B--` (url encoded version of `' or name = 'Trainers';--`) and go to that page, then you will be able to update name of another record, which you may not have access to. Or you can simply encode `' or 1=1;--` (which results in `/sql3?item=%27+or+1%3D1%3B--`) and it will update all records of that table;
- Get database tables schema. Go to "SQL Injection 4". You will see a list of items in the database, which you can filter with "Search query" input. Try inserting `' union select sql from sqlite_master; --` - this will turn to system table `sqlite_master` (for other databases there are similar ones). This table contains information about all other tables' initialization scripts, which is all stored in `sql` column.

#### Web-app

App itself
