def test_eq(test_name, actual, expected):
    if actual != expected:
        print(f"Test '{test_name}' failed:")
        print(f"    actual:     '{actual}''")
        print(f"    expected:   '{expected}'")
    else:
        print(f"Test '{test_name}' passed'")

def test_err(test_name, func, expected_error_type):
    error = None
    try:
        func()
    except Exception as err:
        error = err
    
    if type(error) == expected_error_type:
        print(f"Test '{test_name}' passed")
    else:
        print(f"Test '{test_name}' failed")
        print(f"    actual error:           {error}")
        print(f"    type of actual error:   {type(error)}")
        print(f"    expected error type:    {expected_error_type}")