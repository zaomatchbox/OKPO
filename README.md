### Labs description:

#### McCabe

McCabe metric for Python source code is calculated. Paste your Python source into `textarea` and click on `Calculate McCabe`. You will see code graph and control flow graph below with metric value mentioned in `McCabe: <value>` section

#### SQL Injections

- using operator `union`. Go to "SQL Injection 1" tab. You will see a list of items in the database, which you can filter with "Search query" input. However, adding to the input query term `' union select first_name from auth_user; --` you can grab users info.
- Verification bypass via boolean operators. Go to "SQL Injection 2" tab. You can login to the system if you enter the right login/password. Database users: `User1 / password`, `root / password`, `User2 / password`. If login succeeded, you will receive a green badge, else it will be read. Entering `') OR 1=1; --` in *password* field along with existing user login or `') OR 1=1; --` in *login* field with any password field will result in your login step completed (you will receive green badge).


#### Web-app

App itself
