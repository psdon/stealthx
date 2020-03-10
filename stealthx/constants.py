from dotmap import DotMap

subscription_plan = {
    "FREE": {
        "price": 0,
        "type": "FREE",
        "token": 100,
    },
    "ELITE_MEMBER": {
        "price": 500,
        "type": "ELITE_MEMBER",
        "token": 1000,
    },
    "GUARDIAN_MEMBER": {
        "price": 1000,
        "type": "GUARDIAN_MEMBER",
        "token": 2000,
    },
    "ROYAL_MEMBER": {
        "price": 2000,
        "type": "ROYAL_MEMBER",
        "token": 4000,
    }
}

subscription_plan = DotMap(subscription_plan)

RSA_PUB_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAj9WmtKBf0k7A0AQoKD8X
hifiW9UQSZ3b8QS3bKC78ixd/5JYfvYnG98PRLmzx8O4lbEULFs9MyMwQybjfHoI
XoRXIrzxcoOWrb+ZYI2JHhiRNyqq/Ei4lH33ujU/wx/BGEuVg4h0+AOOpaTzMAZS
QVVin/lYm7i/YTtz02r2c3Wn3t0P3QClH5HZXTQLuxKR6Tbbb3JmFlRVnCtz+nx8
8LiFRVTL1yCTKsmb7cWrHM7CHSEeqwRC1okIeN4HVxPVkmliHIaP4Wi9K5OYFm7y
hcR5mDFjCsq6wyL4uwXUQ7iSghz9dAihWtQwt3p94qNTXtwjaqRsRPRQDVFldVfw
pt25he1hazp0WT1m2owTUW7QJwnr36ybBf7Vsa85WI/mGwRRk8SPF7/xDBJl/JIc
DFTQDu9rE6K7d+o8FxazdSljEc3ItgHxjXZLsriZ6zbvutkou+kikxndGwRv36jm
zH5PGFGmYpPQW1Ua1l2SY7S/9r5d8kbi8ZXDfFT59JjnrCOea+JJbDqFztZNwzyG
p+wJrdhP98EkHnS/HKmCDMEZBImrceUCghMRFpe/eJxendjf+IhHY7UGrP/bbNCw
NJo/721CMW0yZQgVkMHr5lYTkX1iu0kver2AA41W7dvVhOzrx9rhyuDA0b/848Rh
iodwpcAQ0tDp6gy7qt1iN5kCAwEAAQ==
-----END PUBLIC KEY-----"""