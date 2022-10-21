#!/usr/bin/env python

import json
import logging

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = "9932b7b330ae3a9f1ca3c18322564030ac5bd0480226ad0171bdd3c13ec57823"


def lambda_handler(event, context):
    logging.basicConfig(level=logging.DEBUG)
    try:
        body = json.loads(event["body"])

        signature = event["headers"]["x-signature-ed25519"]
        timestamp = event["headers"]["x-signature-timestamp"]

        # validate the interaction

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        message = timestamp + json.dumps(body, separators=(",", ":"))

        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {"statusCode": 401, "body": json.dumps("invalid request signature")}

        # handle the interaction

        msg_type = body["type"]

        if msg_type == 1:
            logging.debug("Got a PING")
            return {"statusCode": 200, "body": json.dumps({"type": 1})}
        elif msg_type == 2:
            logging.debug("Got type 2")
            result = command_handler(body)
            logging.debug(result)
            return result

        return {"statusCode": 400, "body": json.dumps("unhandled request type")}
    except:
        raise


def command_handler(body):
    command = body["data"]["name"]

    if command == "grump":
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "type": 4,
                    "data": {
                        "tts": False,
                        "content": "Grump grumpy grumpy, I'm a grumpy bot.  Kiss my butt.",
                        "embeds": [],
                        "allowed_mentions": {"parse": []},
                    },
                }
            ),
        }

    return {"statusCode": 400, "body": json.dumps("unhandled command")}
