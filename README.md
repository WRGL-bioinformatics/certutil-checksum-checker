# checksum_checker

Python script to check backup hashes which have been createds with certUtil but don't have a simple checking function available.

## TODO

1. Check file is expected format (so we can check all files in a folder without relying on extension)
2. Get hash algorithm used
3. Get target filename
4. Get original checksum
5. Generate new checksum with same algorithm
6. Confirm hashes match
7. Generalise to work across all files in a folder
8. Build an interface to simplify usage.
9. Maybe build the actual backup generation into this program?
