# pgitHash

### What is it?
pseudo git hasher (or short pgitHash), is a small utility to create a .xlsx database to *track files*.

pgitHash is meant to help with manual backups.

Let's say, you have two external USB SSD, `disk1` is used as daily drive, `disk2` as backup drive, both have 1 TB of capacity.

Making a backup every day or every week isn't convenient, is likely you'll spend a lot of time 
researching which files you modified, renamed, deleted or created.

Backing up `disk1` every month seems like a better idea, but it's easier just format `disk2`and 
clone `disk1` into, but well, there is a problem: both are **SSD**, that means that formatting and 
re-writing everything will wear `disk2` faster than just copy, delete or rename manually 
every modified file.

That's why pgitHash emerges, to tell you the differences between those disks and apply any 
change to your backup drive.


### What it does?
Given a path, explores and creates hashes for all files found, then writes all data to databaseN.xlsx file:

Database1 | [ b1 ]
--- | ---
Hash | Path
4acc8e0d6e2084a8e32af7050071eba9 | /Path/To/File1
136b4753c38a7606c243cec3cfa15316 | /Path/To/File2
9db2348a1b4126ebcaacc8cf74197b70 | /Path/To/File3
... | ...

Once you have one, you can re-run pgithash to get another .xlsx file (usually some time after).

Database2 | b2
--- | ---
Hash | Path
1c1c96fd2cf8330db0bfa936ce82f3b9 | /Path/To/File2
9db2348a1b4126ebcaacc8cf74197b70 | /Path/To/file3
aa874662b131efc7bb49a57fceaf61ae | /Path/To/File4
... | ...

With two or more databases you can compare them and obtain their differences like, created, deleted, renamed and changed files.

Database | differences of b2 (newer) and b1 (older) | . 
--- | --- | ---
Hash | Path | Notes
4acc8e0d6e2084a8e32af7050071eba9 | /Path/To/File1 | Deleted
1c1c96fd2cf8330db0bfa936ce82f3b9 | /Path/To/File2 | Changed
9db2348a1b4126ebcaacc8cf74197b70 | /Path/To/file3 | Renamed
aa874662b131efc7bb49a57fceaf61ae | /Path/To/File4 | Added
... | ...

Unlike git, **pgitHash can't revert changes to an older version.**
Instead, psgitHash will _"push"_ all changes to the backup disk.

### To do
- [x] Add potato license
- [x] Write README
- [x] Write _pseudo-database creation_ functionality
- [ ] Write _pseudo-database comparison_ functionality
- [ ] Write _apply changes_ functionality
- [ ] Add dependencies installer
- [ ] Profit???
