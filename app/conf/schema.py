#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: cachetfail2ban

json_schema = """
{
    "$ref": "#/definitions/Cachetfail2Ban",
    "definitions": {
        "Cachetfail2Ban": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "api_token": {
                    "type": "string"
                },
                "api_url": {
                    "type": "string"
                }
            },
            "required": [
                "api_token",
                "api_url"
            ],
            "title": "cachetfail2ban"
        }
    }
}
"""