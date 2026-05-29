
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing a password (e.g., when a user signs up)
password = "joe"
hashed = generate_password_hash(password)
print(hashed)
# Output looks like: scrypt:32768:8:1$abc...$def... (long string)

# Store `hashed` in your database, NOT the plain password

# Later, verifying a password (e.g., at login)
is_valid = check_password_hash(hashed, "joe")
print(is_valid)  # True

is_valid = check_password_hash(hashed, "wrongPassword")
print(is_valid)  # False