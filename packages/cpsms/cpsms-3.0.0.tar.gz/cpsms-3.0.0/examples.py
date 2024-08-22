"""Examples for using the CPSMS gateway package."""

import cpsms


# This will send text messages to Bob and Carol respectively. On their
# devices, the sender will shown as "Alice".

gateway = cpsms.Gateway("username", "password", "Alice")
gateway.send("4512345678", "Hello Bob")
gateway.send("4587654321", "Hello Carol")

# The `.send()` method will return the response from the SMS gateway. Have a
# look at the CPSMS documentation to see what responses look like:
# <https://api.cpsms.dk/documentation/index.html#send>
