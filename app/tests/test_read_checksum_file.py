import pytest
from app.functions.read_checksum_file import ChecksumFile


@pytest.fixture
def test_file():
    return ChecksumFile("TESTDATA/TEST.zip.md5")


def test_can_open_file(test_file):
    """Give a filename and open the file"""
    assert test_file.current_file_exists


def test_can_open_target_file(test_file):
    """Give a filename and open the file"""
    assert test_file.target_file_exists


def test_get_hash_algorithm(test_file):
    """Get the correct hash algorithm used

    For TEST.zip.md5 this should be SHA1
    """
    assert test_file.hash_used == "SHA1"


def test_get_file_name(test_file):
    """Get the name of the hashed file"""
    assert test_file.file_name == "TEST.zip"


def test_get_hash_from_file(test_file):
    """Get the target file hash from it's checksum file"""
    test_hash = "24 21 a3 7b ee b0 7e ab fd 0a 5b d2 44 10 ca 42 c5 17 e4 bd"
    assert test_file.original_hash == test_hash


def test_hash(test_file):
    # test_hash_file = "TESTDATA/TEST.zip"
    # test_hash_algorithm = "sha1"
    test_hash = "24 21 a3 7b ee b0 7e ab fd 0a 5b d2 44 10 ca 42 c5 17 e4 bd"
    # We have to manually remove spaces here, but will test a comparison function
    # separately which will do this for us
    test_hash = test_hash.replace(" ", "")
    # assert test_file.hash(test_hash_file, test_hash_algorithm) == test_hash
    assert test_file.new_hash == test_hash


def test_compare_hash(test_file):
    test_hash_file = "TESTDATA/TEST.zip"
    test_hash_algorithm = "sha1"
    test_hash1 = "24 21 a3 7b ee b0 7e ab fd 0a 5b d2 44 10 ca 42 c5 17 e4 bd"
    test_hash2 = test_file.hash(test_hash_file, test_hash_algorithm)
    assert test_file.compare_hash(test_hash1, test_hash2) == True
