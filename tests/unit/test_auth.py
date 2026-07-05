from app.core.security import generate_otp, get_token_hash

def test_generate_otp():
    otp = generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()

def test_get_token_hash():
    token = "random_token_123"
    hashed = get_token_hash(token)
    assert hashed != token
    assert len(hashed) == 64  # SHA-256 hex digest length
