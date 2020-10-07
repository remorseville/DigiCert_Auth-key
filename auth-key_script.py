import hmac
import hashlib


# DigiCert AuthKey
auth_key = '4D0404C6_BRING_YOUR_OWN_KEY_3391ED9C8740C855391FBA'


# CSR is formatted as a single string. No ---Begin Certificate Request-- or ---End Certificate Request--
csr = 'MIIElzCCAn8CAQAwJjELMAkGA1UEBhMCVVMxFzAVBgNVBAMMDmludmVydq3+JzeqUpO4krTlJNQDc4+EanNTgAP/RvAlIpxsHMFZHxExR64twCxlSLtCl3n6TIjpCERgCMYjv5LykPByplgfLQYT9txeIYMw7PilyM9wn1TDaxxfE----omitted----UjkFpdMHryNRXvyTvjYFp5oB+y5zUawxeqpaU1Kr1H+lP4fsFRbTE8iPf7AGwGaOsDK4+ru1HC8dgwid3k3qrkkrTxHJhHh3YTmK93me56yNgnLX7H+8V7eXGHEfP/cYVOL2Ju5TmopyF2szLiVxXeKZksZL4fchFnGFSRZb5xFQyVNTwbU2V'


# Format YYYY/MM/DD/hh/mm/ss
timestamp = '20210812000000'


# Converts a positive integer into a base36 string
def int_to_base36(num):
  assert num >= 0
  digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  res = ''
  while not res or num > 0:
    num, i = divmod(num, 36)
    res = digits[i] + res
  return res


# If base36_hash length is < 50, prepend with zeros
def less_then_check(base36_hash):
  for i in range(0, len(base36_hash)):
    if not len(base36_hash) == 50:
      base36_hash = "0" + base36_hash[0:]
  return base36_hash


# HMAC.SHA256 > base10 > base36 Hashing > String length check
def hashing(auth_key, csr, timestamp):

  secret = timestamp + csr
  digest = hmac.new(bytes(auth_key, encoding='utf-8'), msg=bytes(secret, encoding='utf-8'), digestmod=hashlib.sha256).hexdigest()
  print("SHA256 Hex: ", digest, "\n")

  decimal_hash = int(digest, 16)
  print("Base10 Decimal Hash: ", decimal_hash, "\n")


  base36_hash = int_to_base36(decimal_hash)
  print("Base36 Hash: ", base36_hash, "\n")

  return less_then_check(base36_hash)


# Combining of the timestamp and base36 hash > Request Token
def request_token(auth_key, csr, timestamp):

  valid_hash = hashing(auth_key, csr, timestamp)
  # Construct final request token
  my_token = timestamp + valid_hash
  print("Request Token: ", my_token.lower())


request_token(auth_key, csr, timestamp)
