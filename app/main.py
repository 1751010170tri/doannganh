from flask import render_template, redirect, request, flash, url_for,session
from flask_login import login_user
from app import app, login
from app.models import *
import hashlib
import time


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        if user:
            if user.type == 0:
                login_user(user=user)
            if user.type == 1:
                return render_template("user/menu.html")
    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route("/themhs", methods=['GET', 'POST'])
def insert():

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gioitinh = request.form['gioitinh']
        diachi = request.form['diachi']
        email = request.form['email']
        lop = Lop.query.get(l)
        birth = request.form['birth']
        l = request.form['lop_id']
        s = QuyDinh.query.get(1)

        if lop.siso < s.siso:
            my_data = HocSinh(firstname, lastname, gioitinh, diachi, email, birth, lop.id)
            db.session.add(my_data)
            db.session.commit()
            lop.siso = lop.siso + 1
            db.session.commit()
            flash("Thêm Học Sinh Thành Công")
            return redirect(url_for('insert'))
        else:
            flash("Đã Đủ Số Lượng Học Sinh")
            return redirect(url_for('insert'))
    lop = db.session.query(Lop).all()
    return render_template("user/themhs.html",Lop = lop)


@app.route("/dslop", methods=['GET', 'POST'])
def dslop():
    lop = db.session.query(Lop).all()
    return render_template("user/danhsachlop.html", lop=lop)


@app.route("/xemct",methods=['GET', 'POST'])
def show():

    id_lop = int(request.args.get("id"))
    l = Lop.query.get(id_lop)
    hs = db.session.query(HocSinh).all()
    return render_template("user/chitiet.html", id_lop=l.id,lp = l, hocsinh=hs)


@app.route("/diemmon", methods=['GET', 'POST'])
def hocsinh():
    hocsinh = db.session.query(HocSinh).all()

    hoc = db.session.query(Hoc).all()
    return render_template("user/diemmon.html", hocsinh=hocsinh, hoc=hoc)


if __name__ == '__main__':
    app.run(debug=True)
