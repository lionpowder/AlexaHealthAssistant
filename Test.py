from main import lambda_handler
import logging

intent_request = {
    "session": {
        "sessionId": "SessionId.1d496c02-4651-48ac-82db-cd7ffde93505",
        "application": {
            "applicationId": "amzn1.ask.skill.b400ea3a-6c3d-4f67-b134-74c5e8b6dc5f"
        },
        "attributes": {},
        "user": {
            "userId": "amzn1.ask.account.AGYDM7AIX4QTMTL3Z4OBVJC5YYQVE4RATGCXOZ4EXOF7QL5S65CK5XJYW7S7XVDWS6RHGR33S6AGXEXHT3MHU3ESXX67HS4YLN5PE5BPFDSU55SSVKNF4H6YPQA5JBWBKO7JLWZNEXSYDLZPE4BNQIMPMKKLY7FDUY6LVWI3TNN2SE47BNTANKGIUSZMHNXNFO7OPDVWOPJAPVI"
        },
        "new": True
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "EdwRequestId.f3c10a4e-6348-4502-af23-44101c7b5a43",
        "locale": "en-US",
        "timestamp": "2017-07-14T01:27:17Z",
        "intent": {
            "name": "CreateUserProfile",
            "slots": {
                "gender": {
                    "name": "gender"
                    # "value": "M"
                },
                "user_name": {
                    "name": "user_name"
                    # "value": "test_user"
                },
                "pregnancy": {
                    "name": "pregnancy"
                    # "value": False
                },
                "user_age": {
                    "name": "user_age"
                    # "value": 20
                }
            }
        }
    },
    "version": "1.0"
}

launch_request = {
    "session": {
        "sessionId": "SessionId.aa1193f3-26fb-4a3e-a57f-9d94001f6521",
        "application": {
            "applicationId": "amzn1.ask.skill.b400ea3a-6c3d-4f67-b134-74c5e8b6dc5f"
        },
        "attributes": {},
        "user": {
            "userId": "amzn1.ask.account.AGYDM7AIX4QTMTL3Z4OBVJC5YYQVE4RATGCXOZ4EXOF7QL5S65CK5XJYW7S7XVDWS6RHGR33S6AGXEXHT3MHU3ESXX67HS4YLN5PE5BPFDSU55SSVKNF4H6YPQA5JBWBKO7JLWZNEXSYDLZPE4BNQIMPMKKLY7FDUY6LVWI3TNN2SE47BNTANKGIUSZMHNXNFO7OPDVWOPJAPVI"
        },
        "new": True
    },
    "request": {
        "type": "LaunchRequest",
        "requestId": "EdwRequestId.5490989e-8c05-4db5-acec-4ebbcf9826db",
        "locale": "en-US",
        "timestamp": "2017-07-16T01:16:11Z"
    },
    "version": "1.0"
}


def main():
    print(lambda_handler(launch_request, {}))


if __name__ == "__main__":
    logging.basicConfig()
    main()