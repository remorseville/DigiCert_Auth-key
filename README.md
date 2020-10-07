<h1 id="digicert-auth-key---instant-issuance">DigiCert Auth-Key - Instant Issuance</h1>
<p>Per DigiCert’s documention (<a href="https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/">https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/</a>) there is a process where you can create the domain validation token prior to submitting an order for an SSL certificate. The goal here is to have the HTTP or DNS validation in place prior to any order being submitted so it is instantly checked and the certificate issues.</p>
<p>The process itself requires a few steps. An “auth_key” is needed from your DigiCert account and there is also a hashing function that needs to be completed to get your token. This script is an example of how to obtain said token based on the documentation provided. (<a href="https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/#how-to-generate-your-request-token">https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/#how-to-generate-your-request-token</a>)</p>
<blockquote>
<p>How to generate your request token</p>
<ol>
<li>Construct the secret to be hashed by prepending the timestamp to your PEM-formatted CSR.</li>
<li>Hash the secret using HMAC-SHA256 with your AuthKey as the key.</li>
<li>Convert the resulting hexadecimal hash to a decimal (base10) hash value.</li>
<li>Convert the decimal hash value to a base36 hash value.</li>
<li>Make sure the base36 hash value is at least 50 characters long. If not, prepend with zeros (<code>0</code>) until it is 50 characters long.</li>
<li>Construct the final request token by prepending the timestamp to the base36 hash value.</li>
</ol>
</blockquote>
<p>Here’s what the process looks like in Python.</p>
<pre><code>import hmac
import hashlib

\# DigiCert AuthKey
auth_key = '4D0404C6_BRING_YOUR_OWN_KEY_3391ED9C8740C855391FBA'

\# CSR is formatted as a single string. No ---Begin Certificate Request-- or ---End Certificate Request--
csr = 'MIIElzCCAn8CAQAwJjELMAkGA1UEBhMCVVMxFzAVBgNVBAMMDmludmVydq3+JzeqUpO4krTlJNQDc4+EanNTgAP/RvAlIpxsHMFZHxExR64twCxlSLtCl3n6TIjpCERgCMYjv5LykPByplgfLQYT9txeIYMw7PilyM9wn1TDaxxfE----omitted----UjkFpdMHryNRXvyTvjYFp5oB+y5zUawxeqpaU1Kr1H+lP4fsFRbTE8iPf7AGwGaOsDK4+ru1HC8dgwid3k3qrkkrTxHJhHh3YTmK93me56yNgnLX7H+8V7eXGHEfP/cYVOL2Ju5TmopyF2szLiVxXeKZksZL4fchFnGFSRZb5xFQyVNTwbU2V'

\# Format YYYY/MM/DD/hh/mm/ss
timestamp = '20210812000000'


\# Converts a positive integer into a base36 string
def int_to_base36(num):
    assert num &gt;= 0
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''
    while not res or num &gt; 0:
        num, i = divmod(num, 36)
        res = digits[i] + res
    return res


\# If base36_hash length is &lt; 50, prepend with zeros
def less_then_check(base36_hash):
    for i in range(0, len(base36_hash)):
        if not len(base36_hash) == 50:
            #print(len(base36_hash))
            base36_hash = "0" + base36_hash[0:]
            #print(base36_hash)
    return base36_hash


\# HMAC.SHA256 &gt; base10 &gt; base36 Hashing &gt; String length check
def hashing(auth_key, csr, timestamp):

    secret = timestamp + csr
    digest = hmac.new(bytes(auth_key, encoding='utf-8'), msg=bytes(secret, encoding='utf-8'), digestmod=hashlib.sha256).hexdigest()
    print("SHA256 Hex: ", digest, "\n")
decimal_hash = int(digest, 16)
print("Base10 Decimal Hash: ", decimal_hash, "\n")

base36_hash = int_to_base36(decimal_hash)
print("Base36 Hash: ", base36_hash, "\n")

return less_then_check(base36_hash)


\# Combining of the timestamp and base36 hash &gt; Request Token
def request_token(auth_key, csr, timestamp):

    valid_hash = hashing(auth_key, csr, timestamp)
    # Construct final request token
    my_token = timestamp + valid_hash
    print("Request Token: ", my_token.lower())


request_token(auth_key, csr, timestamp)
</code></pre>
<p>Example of the output:</p>
<pre><code>SHA256 Hex:  2ea087548b2a2XXXXXXXXXX836266ed9e5c8e2b3f0XXX 

Base10 Decimal Hash:  2109002058024XXXXXXXXXX069226682708402040264171539245279903731XXXXX 

Base36 Hash:  15U4B17YMW9XXXXXXXXXXMFFUHTYB2Z0FA72JB5MWMI8 

Request Token:  20210812000000XXXXXXXXXXtvh6o11e6fzmffuhtyb2z0fa72jb5XXXXX
</code></pre>
<p>From here the token can be used to prepare the DNS or HTTP method and continue to submit the order! (<a href="https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/#dns-txt">https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/#dns-txt</a>)</p>

