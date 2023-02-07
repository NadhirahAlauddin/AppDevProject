from flask import Flask, render_template, request, redirect, url_for
from Forms import  RegisterForm
import shelve, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
#Secures session cookie, Important for production environment/deployment
app.config["SECRET_KEY"] = "secretkey"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        #return redirect(url_for('retrieve_users'))
    return render_template('login.html')

#

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    register_form = RegisterForm(request.form)
    if request.method == 'POST' and register_form.validate():
        regUsers_dict = {}
        db = shelve.open('Users.db', 'c')

        try:
            regUsers_dict = db['Registered Users']
        except:
            print("Error in retrieving Registered Users from Users.db.")

        register_users = User.User(register_form.first_name.data, register_form.last_name.data,
                         register_form.gender.data, register_form.email_add.data, register_form.username.data, register_form.password.data, register_form.confirm_password.data)
        regUsers_dict[register_users.get_user_id()] = register_users
        db['Registered Users'] = regUsers_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('register.html', form=register_form)



@app.route('/retrieveUsers')
def retrieve_users():
    regUsers_dict = {}
    db = shelve.open('Users.db', 'r')
    regUsers_dict = db['Registered Users']
    db.close()

    regUsers_list = []
    for key in regUsers_dict:
        register_users = regUsers_dict.get(key)
        regUsers_list.append(register_users)

    return render_template('retrieveUsers.html', count=len(regUsers_list), regUsers_dict=regUsers_list)
#
#
#
@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = RegisterForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        regUsers_dict = {}
        db = shelve.open('Users.db', 'w')
        regUsers_dict = db['Users']

        user = regUsers_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email_add(update_user_form.email_add.data)
        user.set_username(update_user_form.username.data)
        user.set_gender(update_user_form.gender.data)
        user.set_pwd(update_user_form.password.data)
        user.set_confirm_pwd(update_user_form.confirm_password.data)

        db['Users'] = regUsers_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        regUsers_dict = {}
        db = shelve.open('user.db', 'r')
        regUsers_dict = db['Users']
        db.close()

        user = regUsers_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email_add.data = user.get_email_add()
        update_user_form.username.data = user.get_username()
        update_user_form.password.data = user.get_pwd()
        update_user_form.confirm_password.data = user.get_confirm_pwd()
        return render_template('updateUser.html', form=update_user_form)



@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')




if __name__ == '__main__':
    app.run()

