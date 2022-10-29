# Library Management System (With Django)
A demo app simulating some operations for the management of an online library

## Technical Implementations Include
- Create, Read, Update, Delete
- Basic User Authentication
- ClassViews and Mixins
- User Permissions:
>- at model-level (general user permissions)

>- at object-level (so users have individual/private access specific to their own account)
- User groups
- Custom Permissions
- Custom User Model (Simple case: via AbstractUser)
- global search and custom queryset
- Startup Script (Perform tasks at startup, e.g creating groups and custom permissions if they don't exist)

## Further Notes
- the project currently has a secret key exposed within it. it is left there intentionally and isn't used in production

