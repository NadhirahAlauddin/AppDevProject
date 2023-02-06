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
def register():
    register_form = RegisterForm(request.form)
    if request.method == 'POST' and register_form.validate():
        registered_dict = {}
        db = shelve.open('registered.db', 'c')

        try:
            registered_dict = db['Registered Users']
        except:
            print("Error in retrieving Registered Users from registered.db.")

        register = User.Register(register_form.email_address.data, register_form.username.data,
                         register_form.password.data, register_form.confirm_password.data)
        registered_dict[register.get_register_id()] = register
        db['Registered Users'] = registered_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('register.html', form=register_form)



# @app.route('/retrieveUsers')
# def retrieve_users():
#     users_dict = {}
#     db = shelve.open('user.db', 'r')
#     users_dict = db['Users']
#     db.close()
#
#     users_list = []
#     for key in users_dict:
#         user = users_dict.get(key)
#         users_list.append(user)
#
#     return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)
#
#
#
# @app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
# def update_user(id):
#     update_user_form = CreateUserForm(request.form)
#     if request.method == 'POST' and update_user_form.validate():
#         users_dict = {}
#         db = shelve.open('user.db', 'w')
#         users_dict = db['Users']
#
#         user = users_dict.get(id)
#         user.set_first_name(update_user_form.first_name.data)
#         user.set_last_name(update_user_form.last_name.data)
#         user.set_gender(update_user_form.gender.data)
#         user.set_membership(update_user_form.membership.data)
#         user.set_remarks(update_user_form.remarks.data)
#
#         db['Users'] = users_dict
#         db.close()
#
#         return redirect(url_for('retrieve_users'))
#     else:
#         users_dict = {}
#         db = shelve.open('user.db', 'r')
#         users_dict = db['Users']
#         db.close()
#
#         user = users_dict.get(id)
#         update_user_form.first_name.data = user.get_first_name()
#         update_user_form.last_name.data = user.get_last_name()
#         update_user_form.gender.data = user.get_gender()
#         update_user_form.membership.data = user.get_membership()
#         update_user_form.remarks.data = user.get_remarks()
#
#         return render_template('updateUser.html', form=update_user_form)



@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')




if __name__ == '__main__':
    app.run()

