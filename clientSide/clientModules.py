

def splitJsonResp(s):
    """splits a json http response into just the message, used for testing."""
    print(s)
    split= s.split('\"')
    split=split[3]
    return split