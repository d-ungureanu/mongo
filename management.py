from flask import request
import json
from spartan import Spartan

all_spartans_db={}


def read_spartan_from_json():
    if request.is_json:
        spartan_data = request.get_json()

        if len(spartan_data["first_name"]) > 1:
            s_fn = spartan_data["first_name"]
        else:
            return "ERROR: first name should have at least 2 characters."

        if len(spartan_data["last_name"]) > 1:
            s_ln = spartan_data["last_name"]
        else:
            return "ERROR: last name should have at least 2 characters."

        if int(spartan_data["birth_day"]) in range(1, 32):
            s_bd = spartan_data["birth_day"]
        else:
            return "ERROR: Day of birth should be a number between 1 and 31."

        if int(spartan_data["birth_month"]) in range(1, 13):
            s_bm = spartan_data["birth_month"]
        else:
            return "ERROR: Month of birth should be a number between 1 and 12."

        if int(spartan_data["birth_year"]) in range(1900, 2005):
            s_by = spartan_data["birth_year"]
        else:
            return "ERROR: Year of birth should be a number between 1900 and 2004."

        if len(spartan_data["course"]) > 2:
            s_co = spartan_data["course"]
        else:
            return "ERROR: Course name should have at least 3 characters."

        if len(spartan_data["stream"]) > 2:
            s_st = spartan_data["stream"]
        else:
            return "ERROR: Stream's name should have at least 3 characters."
        if check_id_in_db(spartan_data["sparta_id"]):
            return "ID already in database."
        else:
            s_id = spartan_data["sparta_id"]
        temp_spartan = Spartan(s_id, s_fn, s_ln, s_bd, s_bm, s_by, s_co, s_st)
        return temp_spartan
    else:
        return None

