## A database driver for Django to connect to an GBase 8s database via pyodbc.  

**Some limitations**:

- Does not support default values  
- GBase 8s automatically creates indexes on foreign keys, but Django attempts to do that
  manually; the current implementation here just attempts to catch the error on index
  creation. It may unintentionally catch other index creation errors where the index
  already exists.

### Release History  

Version 1.10.2

- Add datatypes support

Version 1.10.1  

- Fork from django_informixdb  
- Fix 'unsupported column type -114'
