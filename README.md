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
<p>Here’s what the process looks like in Python:</p>
<p><a href="https://github.com/remorseville/DigiCert_Auth-key/blob/main/auth-key_script.py">auth_key-script.py</a></p>
<p>Example of the output:</p>
<pre><code>SHA256 Hex:  2ea087548b2a2XXXXXXXXXX836266ed9e5c8e2b3f0XXX
Base10 Decimal Hash:  2109002058024XXXXXXXXXX069226682708402040264171539245279903731XXXXX
Base36 Hash:  15U4B17YMW9XXXXXXXXXXMFFUHTYB2Z0FA72JB5MWMI8
Request Token:  20210812000000XXXXXXXXXXtvh6o11e6fzmffuhtyb2z0fa72jb5XXXXX
</code></pre>
<p>From here the token can be used to prepare the DNS or HTTP method and continue to submit the order! (<a href="https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/#dns-txt">https://dev.digicert.com/workflows/dv-certificate-immediate-issuance/#dns-txt</a>)</p>

