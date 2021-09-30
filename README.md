# githook-provenance

A simple githook for the creation of intoto attestations

## Example intoto (iet'6ish) provenance file

```json
{
  "signatures": [
    {
      "key_id": "lhinds@redhat.com",
      "signature": "3066023100c6d133a93fa1c875f0edf5d6e15cf1e9efe056bbfe6b8433d926e8058ec55230dae4704b6878a26687aab3c4c104360d023100f3974fea313fa1360fae058dace08363978b91aa4cc6353bb73896bbfd5028b8435050a36371a124fd3c9823555592d4",
      "client_cert": "-----BEGIN CERTIFICATE-----\nMIIB+DCCAX6gAwIBAgITNVkDZoCiofPDsy7dfm6geLbuhzAKBggqhkjOPQQDAzAq\nMRUwEwYDVQQKEwxzaWdzdG9yZS5kZXYxETAPBgNVBAMTCHNpZ3N0b3JlMB4XDTIx\nMDMwNzAzMjAyOVoXDTMxMDIyMzAzMjAyOVowKjEVMBMGA1UEChMMc2lnc3RvcmUu\nZGV2MREwDwYDVQQDEwhzaWdzdG9yZTB2MBAGByqGSM49AgEGBSuBBAAiA2IABLSy\nA7Ii5k+pNO8ZEWY0ylemWDowOkNa3kL+GZE5Z5GWehL9/A9bRNA3RbrsZ5i0Jcas\ntaRL7Sp5fp/jD5dxqc/UdTVnlvS16an+2Yfswe/QuLolRUCrcOE2+2iA5+tzd6Nm\nMGQwDgYDVR0PAQH/BAQDAgEGMBIGA1UdEwEB/wQIMAYBAf8CAQEwHQYDVR0OBBYE\nFMjFHQBBmiQpMlEk6w2uSu1KBtPsMB8GA1UdIwQYMBaAFMjFHQBBmiQpMlEk6w2u\nSu1KBtPsMAoGCCqGSM49BAMDA2gAMGUCMH8liWJfMui6vXXBhjDgY4MwslmN/TJx\nVe/83WrFomwmNf056y1X48F9c4m3a3ozXAIxAKjRay5/aj/jsKKGIkmQatjI8uup\nHr/+CxFvaJWmpYqNkLDGRU+9orzh5hI2RrcuaQ==\n-----END CERTIFICATE-----",
      "root_cert": "-----BEGIN CERTIFICATE-----\nMIICkzCCAhigAwIBAgITZEh9ey5HONiGvc8tE51Y4styKjAKBggqhkjOPQQDAzAq\nMRUwEwYDVQQKEwxzaWdzdG9yZS5kZXYxETAPBgNVBAMTCHNpZ3N0b3JlMB4XDTIx\nMDkzMDA5Mjg1OVoXDTIxMDkzMDA5NDg1OFowADB2MBAGByqGSM49AgEGBSuBBAAi\nA2IABEoSDsl5YlkwJx3kzna0me8vb1xkwzKV6PHD7Qz1EiVAozyX3NOHLVAGk01J\nzJwrgo0R4yaa10jSCcO7qyr7+geMu1JyRo4wirhf1KpKvaKH1FNdcvVgzHZhWuJC\nCCBXIKOCASgwggEkMA4GA1UdDwEB/wQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcD\nAzAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBRxaDOUo73Dcfico9aBHBTx4x7dyTAf\nBgNVHSMEGDAWgBTIxR0AQZokKTJRJOsNrkrtSgbT7DCBjQYIKwYBBQUHAQEEgYAw\nfjB8BggrBgEFBQcwAoZwaHR0cDovL3ByaXZhdGVjYS1jb250ZW50LTYwM2ZlN2U3\nLTAwMDAtMjIyNy1iZjc1LWY0ZjVlODBkMjk1NC5zdG9yYWdlLmdvb2dsZWFwaXMu\nY29tL2NhMzZhMWU5NjI0MmI5ZmNiMTQ2L2NhLmNydDAfBgNVHREBAf8EFTATgRFs\naGluZHNAcmVkaGF0LmNvbTAKBggqhkjOPQQDAwNpADBmAjEA59/3oz+PsI9qbmcY\ni72edZW5cUcftvXI0uBpshu8Xy0Ugv3IFVenMcc6DPQJ6X3RAjEA4JUEXxkZJwPD\n28UPEokUE8oFhTcGOzHFXq1Jhijm3cmwO5X4reFaHGCDaE4tDFpg\n-----END CERTIFICATE-----"
    }
  ],
  "signed": {
    "_type": "link",
    "byproducts": {},
    "command": [],
    "environment": {},
    "materials": {},
    "name": "step-name",
    "products": {
      "bar.mxsdSEAzl": {
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      }
    }
  }
}

```
## Installation

`cp pre-commit.py .git/hooks`

`chmod +x .git/hooks/pre-commit`
