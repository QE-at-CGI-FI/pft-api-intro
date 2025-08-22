import pytest
import requests
import approvaltests

URL = "https://apichallenges.herokuapp.com/"
TODOS_URL = URL + "todos"
CHALLENGES_URL = URL + "challenges"
XCHAL_URL = URL + "challenger"
SECRET_NOTE_URL = URL + "secret/note"

# CRUD - REST: POST, GET, ...

URL_ZIP = "http://api.zippopotam.us/fi/00380"

# ########################
# A Tour of APIs
##########################

def test_asserting_on_json():
    json_string = {"firstname": "Maaret", "lastname": "Pyhäjärvi"}
    assert json_string['firstname'] == "Maaret"

def test_first_get():
    response = requests.get(URL_ZIP)
    assert response.status_code == 200
    assert response.json()['country'] == "Finland"
    approvaltests.verify_as_json(response.json())


def test_first_get_with_return_header():
    response = requests.get(URL_ZIP)
    assert response.status_code == 200
    approvaltests.verify_as_json(response.headers)

def test_white_house_zip_all():
    response = requests.get(URL_ZIP)
    cleaned_header = {k: v if k != "Last-Modified" else "XXX" for k, v in response.headers.items()}
    cleaned_header = {k: v if k != "Date" else "XXX" for k, v in cleaned_header.items()}
    approvaltests.verify_as_json(cleaned_header)

# ########################
# Tracking progress
##########################

MY_TRACKING_CODE = "e0a13374-e994-4522-830e-16933f345a55"

def test_where_are_we_on_challenges():
    response = requests.get(CHALLENGES_URL,
                            headers={"X-CHALLENGER": f"{MY_TRACKING_CODE}"})
    approvaltests.verify_as_json(response.json())

# ########################
# Score and GET
##########################

'''
Issue a POST request on the `/challenger` end point, with no body, to create a new 
challenger session. Use the generated X-CHALLENGER header in future requests to track challenge completion.
'''
def test_challenge_01(): 
    r = requests.post(XCHAL_URL)
    assert r.status_code == 201
    assert r.headers['X-CHALLENGER'] == "foo"
    #approvaltests.verify(xchal)

'''
Issue a GET request on the `/challenges` end point
'''
def test_challenge_02():
    r = requests.get(CHALLENGES_URL,
                            headers={"X-CHALLENGER": f"{MY_TRACKING_CODE}"})
    approvaltests.verify_as_json(r.json())

'''
Issue a GET request on the `/todos` end point
'''
def test_challenge_03():
    response = requests.get(TODOS_URL,
                            headers={"X-CHALLENGER": f"{MY_TRACKING_CODE}"})
    approvaltests.verify_as_json(response.json())

'''
Issue a GET request on the `/todo` end point should 404 because nouns should be plural
'''
def test_challenge_04():
    r = requests.get(URL + "todo",
                     headers={"X-CHALLENGER": f"{MY_TRACKING_CODE}"})
    assert r.status_code == 404

'''
Issue a GET request on the `/todos/{id}` end point to return a specific todo
'''
def test_challenge_05():
    r = requests.get(TODOS_URL + "/4",
                     headers={"X-CHALLENGER": f"{MY_TRACKING_CODE}"})
    approvaltests.verify_as_json(r.json())

'''
Issue a GET request on the `/todos/{id}` end point for a todo that does not exist
'''
def test_challenge_06():
    r = requests.get(TODOS_URL + "/40",
                     headers={"X-CHALLENGER": f"{MY_TRACKING_CODE}"})
    assert r.status_code == 404 

'''
Issue a GET request on the `/todos` end point with a query filter to get only todos which are 'done'. There must exist both 'done' and 'not done' todos, to pass this challenge.
'''
def test_challenge_07():
    headers = {"X-CHALLENGER": MY_TRACKING_CODE}
    r = requests.get(f"{TODOS_URL}/todos?doneStatus=false", headers=headers)
    assert r.status_code == 200
    approvaltests.verify_as_json(r.json())

# ########################
# Authorization Challenges
##########################

'''
Issue a GET request on the `/secret/note` end point and receive 403 when X-AUTH-TOKEN does not match a valid token
'''
def test_challenge_50():
    pass

'''
Issue a GET request on the `/secret/note` end point and receive 401 when no X-AUTH-TOKEN header present
'''
def test_challenge_51():
    pass

'''
Issue a GET request on the `/secret/note` end point receive 200 when valid X-AUTH-TOKEN used - response body should contain the note'''
def test_challenge_52():
    pass

'''
Issue a POST request on the `/secret/note` end point with a note payload e.g. {"note":"my note"} and receive 200 when valid X-AUTH-TOKEN used. Note is maximum length 100 chars and will be truncated when stored.'''
def test_challenge_53():
    pass

'''
Issue a POST request on the `/secret/note` end point with a note payload {"note":"my note"} and receive 401 when no X-AUTH-TOKEN present
'''
def test_challenge_54():
    pass

'''
Issue a POST request on the `/secret/note` end point with a note payload {"note":"my note"} and 
receive 403 when X-AUTH-TOKEN does not match a valid token
'''
def test_challenge_55():
    pass

'''
Issue a GET request on the `/secret/note` end point receive 200 when using the X-AUTH-TOKEN value 
as an Authorization Bearer token - response body should contain the note'''
def test_challenge_56():
    pass

'''
Issue a POST request on the `/secret/note` end point with a note payload e.g. {"note":"my note"} 
and receive 200 when valid X-AUTH-TOKEN value used as an Authorization Bearer token. Status code 200 received. Note is maximum length 100 chars and will be truncated when stored.
'''
def test_challenge_57():
    pass


'''
Issue a HEAD request on the `/todos` end point
'''
def test_challenge_08():
    pass

'''
Issue a POST request to successfully create a todo
'''
def test_challenge_09():
    pass

'''
Issue a POST request to create a todo but fail validation on the `doneStatus` field
'''
def test_challenge_10():
    pass

'''
Issue a POST request to create a todo but fail length validation on the `title` field because your title exceeds maximum allowable characters.
'''
def test_challenge_11():
    pass

'''
Issue a POST request to create a todo but fail length validation on the `description` because your description exceeds maximum allowable characters.
'''
def test_challenge_12():
    pass

'''
Issue a POST request to create a todo with maximum length title and description fields.
'''
def test_challenge_13():
    pass

'''
Issue a POST request to create a todo but fail payload length validation on the 
`description` because your whole payload exceeds maximum allowable 5000 characters.
'''
def test_challenge_14_broken():
    pass

'''
Issue a POST request to create a todo but fail validation because your payload contains an 
unrecognised field.
'''
def test_challenge_15():
    pass

'''
Issue a PUT request to unsuccessfully create a todo
'''
def test_challenge_16():
    pass

'''
Issue a POST request to successfully update a todo
'''
def test_challenge_17():
    pass

'''
Issue a POST request for a todo which does not exist. Expect to receive a 404 response.
'''
def test_challenge_18():
    pass

'''
Issue a PUT request to update an existing todo with a complete payload i.e. title, description and donestatus.
'''
def test_challenge_19():
    pass

'''
Issue a PUT request to update an existing todo with just mandatory items in payload i.e. title.
'''
def test_challenge_20():
    pass

'''
Issue a PUT request to fail to update an existing todo because title is missing in payload.
'''
def test_challenge_21():
    pass

'''
Issue a PUT request to fail to update an existing todo because id different in payload.
'''
def test_challenge_22():
    pass

'''
Issue a DELETE request to successfully delete a todo
'''
def test_challenge_23():
    pass


'''
Issue an OPTIONS request on the `/todos` end point. You might want to manually check the 'Allow' header in the response is as expected.'''
def test_challenge_24():
    pass

'''
Issue a GET request on the `/todos` end point with an `Accept` header of `application/xml` to receive results in XML format
'''
def test_challenge_25():
    pass

def test_challenge_26():
    pass

def test_challenge_27():
    pass
