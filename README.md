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

Once you have one, you can re-run pgitHash to get another .xlsx file (usually after some time).

Database2 | [ b2 ]
--- | ---
Hash | Path
1c1c96fd2cf8330db0bfa936ce82f3b9 | /Path/To/File2
9db2348a1b4126ebcaacc8cf74197b70 | /Path/To/file3
aa874662b131efc7bb49a57fceaf61ae | /Path/To/File4
... | ...

With two databases you can compare them and obtain their differences like, created, deleted, renamed and changed files.

Database | differences of b1 (older) and b2 (newer) | . 
--- | --- | ---
Hash | Path | Notes
4acc8e0d6e2084a8e32af7050071eba9 | /Path/To/File1 | Deleted
1c1c96fd2cf8330db0bfa936ce82f3b9 | /Path/To/File2 | Changed
9db2348a1b4126ebcaacc8cf74197b70 | /Path/To/file3 | Renamed
aa874662b131efc7bb49a57fceaf61ae | /Path/To/File4 | Added
... | ...

Unlike git, **pgitHash can't revert changes to an older version.**
Instead, psgitHash will _"push"_ all changes to the backup disk.


### Run pgitHash

1. Install Python >= 3.6
2. Clone repo `git clone https://github.com/cdelaof26/pgitHash`
3. Install dependencies `pip install -r requirements.txt`
   > Usually is `pip3 install -r requirements.txt` instead of `pip`
4. Run with `python main.py` or `python3 main.py`


### Know issues
pgitHash can't track moved files

### To do
- [x] Add license
- [x] Write README
- [x] Write _pseudo-database creation_ functionality
- [x] Write _pseudo-database comparison_ functionality
- [ ] Write _apply changes_ functionality
- [x] ~~Add dependencies installer~~ Added `requirements.txt`
- [ ] Add _create tree_ functionality to track files moved
- [ ] Add _switchable hash algorithm_ functionality
- [ ] Profit???


### License

pgitHash is licensed under the MIT license, as included in the [LICENSE](LICENSE) file.
