from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from icecream import ic
ic.configureOutput(prefix=f'______ | ', includeContext=True)

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


############################## LOGIN ROUTES ##############################

##############################
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"

##############################
@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        user_hashed_password = generate_password_hash(user_password)
        
        #ic(user_hashed_password) #user_hashed_password: 'scrypt:32768:8:1$4i9bCS3sOL0FoQzJ$2aba7c881a8b7fcc0b304d218258d843bee3c0fb873168bb320d38bfb1a9646d547f6b833f9b0e17b04c0031328790c60ebb58eee89d2c15b99bbba1cdcc96a3'

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f""" 
        <browser mix-replace="form">{form_signup}</browser>
        <browser mix-redirect="/login">  </browser> """ 

    except Exception as ex:
        ic(ex)

        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "Duplicate entry" in str(ex) and "user_email" in str(ex): 
            error_message = "Email already in the system"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

            # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user: 
            return render_template("page_login.html", user=user, x=x)
        return redirect("/destinations")
    except Exception as ex:
        ic(ex)
        return "ups"



##############################
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user:
            error_message = "Invalid credentials 1"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials 2"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400            

        user.pop("user_password")
        session["user"] = user

        return f"""<browser mix-redirect="/destinations"></browser>"""

    except Exception as ex:
        ic(ex)

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

            # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")
        return render_template("page_profile.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.get("/logout")
def show_logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "ups"


############################## DESTINATION ROUTES ##############################

##############################
@app.get("/destinations")
@x.no_cache
def show_destinations():
    try:
        user = session.get("user", "")
        db, cursor = x.db()
        cursor.execute("SELECT * FROM destinations ORDER BY destination_created_at DESC")
        destinations = cursor.fetchall()
        for dest in destinations:
            dest["destination_date_from"] = x.format_timestamp(dest["destination_date_from"])
            dest["destination_date_to"] = x.format_timestamp(dest["destination_date_to"])
        return render_template("page_destinations.html", user=user, x=x, destinations=destinations)
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/destination/<destination_pk>")
@x.no_cache
def show_destination_edit(destination_pk):
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")
        db, cursor = x.db()
        q = "SELECT * FROM destinations WHERE destination_pk = %s"
        cursor.execute(q, (destination_pk,))
        destination = cursor.fetchone()
        if not destination:
            return redirect("/destinations")
        destination["destination_date_from"] = x.format_timestamp(destination["destination_date_from"])
        destination["destination_date_to"] = x.format_timestamp(destination["destination_date_to"])
        return render_template("page_destination_edit.html", user=user, x=x, destination=destination)
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/destination/create")
@x.no_cache
def show_destination_create():
    try:
        user = session.get("user", "")
        return render_template("page_destination_create.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"

##############################
@app.post("/api-create-destination")
def api_create_destination():
    try: 
        user = session.get("user", "")
        if not user:
            error_message = "You must be logged in"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 401
        destination_user_fk = user["user_pk"]

        destination_title = x.validate_destination_title()
        destination_date_from = x.validate_destination_date_from()
        destination_date_to = x.validate_destination_date_to()
        destination_description = x.validate_destination_description()
        destination_location = x.validate_destination_location()
        destination_country = x.validate_destination_country()

        destination_pk = uuid.uuid4().hex
        destination_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO destinations VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (destination_pk, destination_user_fk, destination_title, destination_date_from, destination_date_to, destination_description, destination_location, destination_country, destination_created_at))
        db.commit()
        return f"""<browser mix-redirect="/destinations"></browser>"""

    except Exception as ex:
        ic(ex)

        if "company_exception destination_title" in str(ex):
            error_message = f"Title {x.DESTINATION_TITLE_MIN} to {x.DESTINATION_TITLE_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception destination_date_from" in str(ex):
            error_message = "Date from is required"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception destination_date_to" in str(ex):
            error_message = "Date to is required"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception destination_description" in str(ex):
            error_message = f"Description max {x.DESTINATION_DESCRIPTION_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception destination_location" in str(ex):
            error_message = f"Location {x.DESTINATION_LOCATION_MIN} to {x.DESTINATION_LOCATION_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception destination_country" in str(ex):
            error_message = f"Country {x.DESTINATION_COUNTRY_MIN} to {x.DESTINATION_COUNTRY_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.delete("/api-delete-destination/<destination_pk>")
def api_delete_destination(destination_pk):
    try:
        user = session.get("user", "")
        if not user:
            error_message = "You must be logged in"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 401

        db, cursor = x.db()
        q = "DELETE FROM destinations WHERE destination_pk = %s"
        cursor.execute(q, (destination_pk,))
        if cursor.rowcount == 0:
            error_message = "Destination not found"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 404
        db.commit()
        return f"""<browser mix-remove="#destination_{destination_pk}"></browser>"""

    except Exception as ex:
        ic(ex)
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.patch("/api-update-destination/<destination_pk>")
def api_update_destination(destination_pk):
    try:
        user = session.get("user", "")
        if not user:
            error_message = "You must be logged in"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 401

        parts = []
        values = []

        destination_title = request.form.get("destination_title", "").strip()
        if destination_title:
            parts.append("destination_title = %s")
            values.append(destination_title)

        destination_date_from = request.form.get("destination_date_from", "").strip()
        if destination_date_from:
            parts.append("destination_date_from = %s")
            values.append(x.validate_destination_date_from())

        destination_date_to = request.form.get("destination_date_to", "").strip()
        if destination_date_to:
            parts.append("destination_date_to = %s")
            values.append(x.validate_destination_date_to())

        destination_description = request.form.get("destination_description", "").strip()
        if destination_description:
            parts.append("destination_description = %s")
            values.append(destination_description)

        destination_location = request.form.get("destination_location", "").strip()
        if destination_location:
            parts.append("destination_location = %s")
            values.append(destination_location)

        destination_country = request.form.get("destination_country", "").strip()
        if destination_country:
            parts.append("destination_country = %s")
            values.append(destination_country)

        if not parts:
            error_message = "No changes provided"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        partial_query = ", ".join(parts)
        values.append(destination_pk)

        q = f"""
            UPDATE destinations
            SET {partial_query}
            WHERE destination_pk = %s
        """

        db, cursor = x.db()
        cursor.execute(q, values)
        db.commit()
        return f"""<browser mix-redirect="/destinations"></browser>"""

    except Exception as ex:
        ic(ex)

        if "company_exception destination_date_from" in str(ex):
            error_message = "Date from is required"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception destination_date_to" in str(ex):
            error_message = "Date to is required"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()