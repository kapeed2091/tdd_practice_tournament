def foo_user_to_headers_converter(foo_user):
    return {
        "API_GATEWAY_AUTHORIZER": {
            "claims": {
                "cognito:username": str(foo_user.username),
                "cognito:id": str(foo_user.id),
                "cognito:role": "PLAYER",
                "custom:registration_type": "USERNAME"
            }
        }
    }
