from werkzeug.utils import redirect
from app import db, admin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user


class User(db. Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    type = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class UserModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


class Khoi(db.Model):
    __tablename__ = "khoi"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    lops = relationship("Lop", backref="khoi", lazy=True)

    def __str__(self):
        return self.name


class KhoiModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


class Lop(db.Model):
    __tablename__ = "lop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    siso = Column(Integer,nullable=False)
    khoi_id = Column(Integer, ForeignKey(Khoi.id), nullable=False)
    hocsinhs = relationship('HocSinh', backref='lop', lazy=True)

    def __str__(self):
        return self.name


class LopModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


class HocSinh(db.Model):
    __tablename__ = "hocsinh"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(50), nullable=False)
    gioitinh = Column(String(10), nullable=False)
    diachi = Column(String(255))
    email = Column(String(100), unique=True)
    ngaysinh = Column(Date, nullable=False)
    lop_id = Column(Integer, ForeignKey(Lop.id), nullable=False)
    bangdiem = relationship("Hoc", backref='hocsinh', lazy=True)



    def __init__(self, firstname, lastname, gioitinh, diachi, email, ngaysinh,lop_id):
        self.firstname = firstname
        self.lastname = lastname
        self.gioitinh = gioitinh
        self.diachi = diachi
        self.email = email
        self.ngaysinh = ngaysinh
        self.lop_id = lop_id

    def __str__(self):
        return self.lastname + " " + self.firstname + " _ " + str(self.ngaysinh) + " _ " + str(self.lop)+ "_" + str(self.id)


class HocSinhModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True
    #form_columns = ('firstname', 'lastname', 'gioitinh', 'diachi','email', 'ngaysinh', )


class MonHoc(db.Model):
    __tablename__ = "monhoc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    diem = relationship("Hoc", backref='monhoc', lazy=True)

    def __str__(self):
        return self.name


class MonHocModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True
    #form_columns = ('id', 'name')


class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tuoimin = Column(Integer, default=0)
    tuoimax = Column(Integer, default=0)
    siso = Column(Integer, default=0)
    diem = Column(Integer, default=0)

    def __str__(self):
        return self.name


class QuyDinhModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


class Hoc(db.Model):
    __tablename__ = "hoc"

    hocsinh_id = Column(Integer, ForeignKey(HocSinh.id), primary_key=True)
    monhoc_id = Column(Integer, ForeignKey(MonHoc.id), primary_key=True)
    ky1_15p = Column(Float, default=0)
    ky1_1tiet = Column(Float, default=0)
    ky1_final = Column(Float, default=0)
    ky2_15p = Column(Float, default=0)
    ky2_1tiet = Column(Float, default=0)
    ky2_final = Column(Float, default=0)



class HocModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


#class HocView(ModelView):
  #  can_export = True
  #  can_set_page_size = True
   # column_display_pk = True
    #form_columns = ('hocsinh', 'monhoc', 'namhoc', 'ky1_15p', 'ky1_1tiet', 'ky1_final', 'ky2_15p', 'ky2_1tiet', 'ky2_final')

   # def is_accessible(self):
     #   return current_user.is_authenticated


admin.add_view(KhoiModelView(Khoi, db.session))
admin.add_view(LopModelView(Lop, db.session))
admin.add_view(HocSinhModelView(HocSinh, db.session))
admin.add_view(MonHocModelView(MonHoc, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(QuyDinhModelView(QuyDinh, db.session))
admin.add_view(HocModelView(Hoc, db.session))

admin.add_view(LogoutView(name="Logout"))
if __name__ == "__main__":
    db.create_all()