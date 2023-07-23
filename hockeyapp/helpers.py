from io import BufferedRandom
import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

class Stick: 
    def __init__(self, brand, size, flex, curve, hand, model):
        self.brand = brand
        self.size = size
        self.flex = flex
        self.curve = curve
        self.hand = hand
        self.model = model
class Skates:
    def __init__(self, brand, size, model):
        self.brand = brand
        self.size = size
        self.model = model
