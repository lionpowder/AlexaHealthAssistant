import logging
from dbUtil import insert_patient
from dbUtil import get_user_info
from dbUtil import get_drug_side_effects

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

required_slots = ['user_name', 'user_age', 'gender']


# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(output, reprompt_text, should_end_session, directives=None):
    ret = {}
    if output is not None:
        ret['outputSpeech'] = {'type': 'PlainText', 'text': output}

    if reprompt_text is not None:
        ret['reprompt'] = {'outputSpeech': {'type': 'PlainText', 'text': reprompt_text}}

    ret['shouldEndSession'] = should_end_session

    if directives is not None:
        ret['directives'] = directives

    return ret


def build_response(session_attr, response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attr,
        'response': response
    }


def dialog_delegate():
    return {"type": "Dialog.Delegate"}


def slot_elicitation(slot_name):
    return {"type": "Dialog.ElicitSlot", "slotToElicit": slot_name}


def get_session_attr(session):
    if 'attributes' in session:
        session_attr = session['attributes']
    else:
        session_attr = {}

    if 'user_info' not in session_attr:
        session_attr['user_info'] = {}

    return session_attr

# --------------- Functions that control the skill's behavior ------------------
def set_profile_in_session(intent, session):

    session_attr = get_session_attr(session)

    for required_slot_item in required_slots:
        if 'value' not in intent['slots'][required_slot_item]:
            return build_response(session_attr, build_speechlet_response(
                output=None, reprompt_text=None,should_end_session=False,
                directives=[dialog_delegate()]))

    for required_slot_item in required_slots:
        session_attr['user_info'][required_slot_item] = intent['slots'][required_slot_item]['value']

    if session_attr['user_info']['gender'] == 'female':
        if 'pregnancy' not in intent['slots'] or 'value' not in intent['slots']['pregnancy']:
            return build_response(
                session_attr=session_attr,
                response=build_speechlet_response(
                    output="are you pregnant?",reprompt_text=None, should_end_session=False,
                    directives=[slot_elicitation("pregnancy")]))

        else:
            session_attr['user_info']['pregnancy'] = intent['slots']['pregnancy']['value'].lower() == 'yes'
    else:
        session_attr['user_info']['pregnancy'] = False

    insert_patient(session_attr['user_info'])

    return build_response(
        session_attr=session_attr,
        response=build_speechlet_response(
            output="I now know your name is {}, and you're a {} years old {}. Your information has been saved.".format(
                session_attr['user_info']['user_name'], session_attr['user_info']['user_age'], session_attr['user_info']['gender']),
            reprompt_text="Is there anything else that I can do for you?",
            should_end_session=False))


def get_side_effects(intent, session):

    session_attr = get_session_attr(session)
    if 'user_name' not in session_attr['user_info'] and 'value' not in intent['slots']['user_name']:
        return build_response(
            session_attr=session_attr,
            response=build_speechlet_response(
                output="Can I get your name please?",
                reprompt_text=None, should_end_session=False,
                directives=[slot_elicitation('user_name')]))
    else:
        session_attr['user_info']['user_name'] = intent['slots']['user_name']['value']

    if not all(slot in session_attr['user_info'] for slot in required_slots):
        session_attr['user_info'] = get_user_info(session_attr['user_info']['user_name'])

    side_effects = get_drug_side_effects(session_attr['user_info'], intent['slots']['drug']['value'])

    return build_response(
        session_attr=session_attr,
        response=build_speechlet_response(
            output=side_effects,
            reprompt_text=None, should_end_session=False))

# --------------- Events ------------------

def on_intent(intent_request, session):
    logger.info("on_intent requestId=%s, sessionId=%s, session=%s, intent=%s", intent_request['requestId'],
                session['sessionId'], str(session), str(intent_request['intent']))

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "CreateUserProfile":
        return set_profile_in_session(intent, session)
    elif intent_name == "GetSideEffects":
        return get_side_effects(intent, session)

    elif intent_name == "AMAZON.HelpIntent":
        return build_response(
            session_attr={},
            response=build_speechlet_response(
                output="Welcome to the medical diagnosis skill set. What can I do for you?",
                reprompt_text="For example, you can get information about drug side effects.",
                should_end_session=False))

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return build_response(
            session_attr={},
            response=build_speechlet_response(
                output="Thank you for trying the medical diagnosis skill set. Have a nice day! ",
                reprompt_text="",
                should_end_session=True))
    else:
        raise ValueError("Invalid intent")


# --------------- Main handler ------------------
def on_session_started(session_started_request, session):
    logger.info("session=%s", str(session))



def on_launch(launch_request, session):
    logger.info("on_launch requestId=%s, sessionId=%s", launch_request['requestId'], session['sessionId'])

    return build_response(
        session_attr={},
        response=build_speechlet_response(
            output="Welcome to the medical diagnosis skill set. What can I do for you?",
            reprompt_text="Sorry I didn't hear from you, is there anything I can do?",
            should_end_session=False))


def on_session_ended(session_ended_request, session):
    logger.log("on_session_ended requestId=%s, sessionId=%s", session_ended_request['requestId'], session['sessionId'])


def lambda_handler(event, context):
    logger.info("event.session.application.applicationId=%s", event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
