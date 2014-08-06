SQL IDE based on hotkeys and kinesthetic memory.  
Project started for easing everyday dummy work in development: showing table description, selecting few fields, sorting and limit output rows.  
Base idea is: kinesthetic memory is fast, when one use keys without thinking (press **e** and see table description) work flow is really lively.
*Position of keys is now discussable, I try set it not by key meaning, but by usage frequency.*

**Database connection and other options set in config.py.**

*Current version work only with MySQL. Current version was tested only under Debian, Ubuntu and Mint. Don't work in MacOS because of different tkinter and tkintertable libraries.*

####Hotkeys:
```
"main" window:
    a: execute query
    d: default select
    e: show description of a table
    f: select from table
    i: select fields
    l: sort table
    o: group by
    r: change sort order
    s: show tables
    u: totally manual query
    x: limit select
    esc: close window

any "select something" window:
    a: accept selected rows
    c: clear selection
    j: move cursor down
    k: move cursor up
    space: select current row

"write text" window:
    wrap field by:
        a: avg()
        c: count()
        d: max()
        f: min()
        s: sum()
    i: change manual and auto mode
    j: move left
    k: move right
```

####Examples: 
I.  
1. Press **d** key.  
2. Choose table using **j** and **k** keys for movement and **space** key for selecting. Also you can use filter string.  
3. Press **a** key for submit.

II.  
1. Press **f** key.  
2. Choose table using **j** and **k** keys for movement and **space** key for selecting.
3. Press **a** key for submit.  
4. Press **i** key.  
5. Select one or several fields.  
6. Press **a** key for submit.  
7. Press **a** key for execution built query.  

III.  
1. Make same steps as in II example. But now choose table and fields that you can use in group by.  
2. Press **o**.  
3. Choose field(s) for group by section.  
4. Press **a** for submit.  
5. Move through fields by **j** and **k** keys. And use **a**, **c**, **d**, **f** or **s** keys for setting aggregate functions.  
6. Press **enter**.  
7. Press **a**.  

IV.  
1. After getting result table you can use **l** key for choosing sort column.  
2. By pressing **r** you can change sort order.  

P.S. A lot of work in progress:
- result table appearance,  
- result table scan hotkeys,
- where clause,
- hint and info windows,
- ways for building query with joins and subqueries,
- update, delete queries,  
- fixing batch of bugs.  
In future I want to add some analyst tools for queries: diagrams as example.