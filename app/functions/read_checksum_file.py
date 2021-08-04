import hashlib
import pathlib
import sys


class ChecksumFile(object):
    def __init__(self, filename=None):
        self.fname = pathlib.Path(filename)
        
        if self.current_file_exists:
            self._hash_used = self.get_hash_used()
            self._file_name = self.get_file_name()
            self._target_path = self.get_file_path()
            self._original_hash = self.get_hash_from_file()
            self._new_hash = self.hash(self._target_path, self.hash_used)
            self._hash_match = False
            if self.compare_hash(self._original_hash, self._new_hash):
                self._hash_match = True
            else:
                self._hash_match = False
        else:
            self._hash_match = False

    def __repr__(self) -> str:
        return f"<ChecksumFile: {self.fname}"

    def __str__(self) -> str:
        return f"<ChecksumFile: {self.fname}"

    @property
    def current_file_exists(self) -> bool:
        """Check the target file exists"""
        # As far as checking that the file is correct, I'm just going to check the
        # extension. There's no real point doing more at this point.
        # Quit on any error here
        if not self.fname.suffix == ".md5":
            sys.exit(1)
        try:
            with open(self.fname) as f:
                f.readline()
            return True
        except FileNotFoundError:
            sys.exit(1)

    @property
    def target_file_exists(self) -> bool:
        """Check the target file exists"""
        try:
            with open(self._target_path, "rb") as f:
                f.readline()
            return True
        except FileNotFoundError:
            print(f"ERROR: Cannot open target file {self._target_path}", file=sys.stderr)
            return False

    @property
    def hash_used(self) -> str:
        """Hash used from the checksum file"""
        return self._hash_used

    @property
    def file_name(self) -> str:
        """Name of hashed file from checksum file"""
        return self._file_name

    @property
    def checksum_file_name(self) -> str:
        """Name of the current checksum file"""
        return self.fname.name

    @property
    def target_path(self) -> str:
        """Return the path to the target file"""
        return self._target_path

    @property
    def original_hash(self) -> str:
        """Checksum hash from the checksum file"""
        return self._original_hash

    @property
    def new_hash(self) -> str:
        """Checksum hash generated from target file"""
        return self._new_hash

    @property
    def hash_ok(self) -> bool:
        """Does the file hash match the calcualted hash?"""
        return self._hash_match

    def get_hash_used(self) -> str:
        """Check the hash algorithm used"""
        with open(self.fname) as f:
            line: str = f.readline().split()[0]
            return line

    def get_file_name(self) -> str:
        """Get the name of the hashed file"""
        with open(self.fname) as f:
            # File name is the last item on the first line
            fname: str = f.readline().split()[-1]
            # Remove all non-alphanumeric characters from the ends of the string
            # NOTE: We have to escape '\' to avoid a warning
            fname = fname.strip("[,.\\:]")
            return fname

    def get_file_path(self) -> str:
        """Get the path to the target file
        relative to the current lcoation of the checksum file"""
        folder_path = pathlib.Path(self.fname).resolve().parent
        target_path = folder_path / self._file_name

        return str(target_path)

    def get_hash_from_file(self):
        """TODO"""
        with open(self.fname) as f:
            # Read the first line, but do nothing
            line = f.readline()
            # The second line contains the hash
            line = f.readline()
            # Remove newlines, etc. from ends of the line
            line = line.strip()
            return line
        return None

    @staticmethod
    def hash(fname, algorithm):
        """Hash the file with the specified algorithm"""

        # Ensure that the algorithm is recognised. Hashlib uses all lower case for
        # it's algorithm names
        try:
            file_hash = hashlib.new(algorithm.lower())
        except ValueError:
            print("ERROR: Hash algorithm not recognised", file=sys.stderr)
            return None

        # Hash the file in chunks, as this is more memory efficient - particularly for
        # larger files like the ones we will want to hash.
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash.update(chunk)

        # The hexdigest is the normal text representation, without any spaces
        # e.g. 2421a3 vs. 24 21 a3
        return file_hash.hexdigest()

    @staticmethod
    def compare_hash(hash1, hash2):
        """Compare hashes, removing spaces if needed"""
        hash1 = hash1.replace(" ", "")
        hash2 = hash2.replace(" ", "")
        return hash1 == hash2
