
    This is variant of registration/login.

In start you need to do:
        1. pip install django-sslserver==0.20 (sslserver in INSTALLED_APPS) or use another sslserver,
            because Facebook, Twitter and Google do not allow work without safe connection.
            (manage.py  runsslserver smaffy.com:8888)

        2. for testing in localhost, you need edit '/etc/hosts' (add "127.0.0.1     smaffy.com")
                    (for Windows:  C:\Windows\System32\Drivers\etc\hosts )

        3. you need connect Database (was used MySql) and create superuser(admin)

        4. add Cron command for daily run 'account/managment/commands/deleteusers.py'

What options are in project?

In project is 2 tipes of account:  classical and social

    1. classical account
        * user need register: unique username + unique email + password +
            Privacy Policy and Terms and Conditions.

            (if email already in use - help for restoring account. registration canceled.
            after input email account: search user, if not password set random,
            return username end link to reset password by email)

        created user and user.profile, send email confirmation.
        now user not confirmed and can not login
        in email get link. now account confirmed and active.

        * now user can:
            1. edit profile
            2. Config login settings (check/connect/disconnect Facebook, Twitter, Google)
            3. Change password
            4. Soft delete (set inactive. In 30 days after last login account will be hard deleted by Cron command. )
            5. Hard delete (just delete from db)
            6. login by username/email + password
            7. reset password, if forgotten it
            8. look in dashboard connections and some data

    2. social account
        * user do not need register: autocreated account, without password.

            In clicking submit user is agreeing to the Privacy Policy and Terms and Conditions

            created user and user.profile, need email confirmation, but not soo important for user.

            now user active, can login only by social login.


            (if email already in use - backend just associate by email with another account, without ceation new user)

        * now user can:
            1. edit profile
            2. Config login settings (check/connect/disconnect Facebook, Twitter, Google, set password)
            3. Set password
            4. ** Can not use soft delete, because "You do not have email or password for restore account."
            5. Hard delete (just delete from db)
            6. login by social_login
            8. look in dashboard connections and some data

        * if user add password and confirm email, user start to be classical.
                It is mean, he can (same like classical):
                                1. edit profile
                                2. Config login settings (check/connect/disconnect Facebook, Twitter, Google)
                                3. Change password
                                4. Soft delete (set inactive. In 30 days after last login account will be hard deleted by Cron command. )
                                5. Hard delete (just delete from db)
                                6. login by username/email + password
                                7. reset password, if forgotten it
                                8. look in dashboard connections and some data


Passwords:

    1. standart reset if forgotten password - send email with link
    2. set password (for user.is_authenticated), if you do not have it.
    3. change, if you have password

    4. no password + no access by social login = set random password and link to reset password by email

2 help for unsolved problems:
    * emailhelp
    * helpAuthAlreadyAssociated

Another content for:
    * user.is_authenticated
    * user.is_active
    * user.profile.is_confirmed
    * user.has_usable_password
    * user.email/ not user.email
    * facebook_login
    * twitter_login
    * google_login


** new problem: "reset password" send email, without check user.