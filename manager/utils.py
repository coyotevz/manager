# -*- coding: utf-8 -*-

from flask import jsonify

def json_response(data, status_code=200, headers=None):
    response = jsonify(**data)
    response.status_code = status_code

    if isinstance(headers, dict):
        response.headers.extend(headers)

    return response
