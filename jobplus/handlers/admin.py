from flask import (Blueprint, render_template, redirect, flash, url_for, request, current_app)
from jobplus.models import (db, User, Jobs)
from jobplus.forms import (UserForm)
from werkzeug.security import (generate_password_hash)

from jobplus.decorator import (delete, ban, unban, admin_required, get_alluser)

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = get_alluser(page, current_app)
    active = 'console'
    return render_template('admin/user_config.html', pagination=pagination, active=active)


@admin.route('/users/adduser', methods=["GET", "POST"])
def user_add():
    """
    添加用户
    Author：little、seven
    :return:
    """
    form = UserForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            email=data["email"],
            password=data["password"],
            username=data["username"],
            phone=data["phone"],
            deleted=0
        )
        db.session.add(user)
        db.session.commit()
        flash("用户新增成功", 'success')
        return redirect(url_for('admin.index'))
    return render_template("admin/user_add.html", form=form)


@admin.route('/users/edituser/<int:id>', methods=["GET", "POST"])
def user_edit(id=None):
    """
    编辑用户
    Author: little、seven
    :param id:
    :return:
    """
    user = User.query.get_or_404(int(id))
    form = UserForm(obj=user)
    if form.validate_on_submit():
        data = form.data
        user.email = data["email"],
        user.password = generate_password_hash(data["password"]),
        user.username = data["username"],
        user.phone = data["phone"],
        db.session.add(user)
        db.session.commit()
        flash("修改成功!", "success")
        return redirect(url_for("admin.index"))
    return render_template("admin/user_edit.html", form=form, user=user)


@admin.route('/users/delteuser/<int:id>', methods=["GET", "POST"])
def user_delete(id=None):
    """
    删除用户(逻辑删除)
    Author: little、seven
    :param id: 用户id
    :return:
    """
    user = delete(User, int(id))
    if user:
        flash("删除用户成功!", "success")
        return redirect(url_for('admin.index'))


@admin.route('/users/unbanuser/<int:id>')
def user_unban(id=None):
    """
    启用用户(启用用户)
    :param id:
    :return:
    """
    user = unban(User, int(id))
    if user:
        flash("启用用户成功", "success")
        return redirect(url_for('admin.index'))


@admin.route('/users/banuser/<int:id>')
def user_ban(id=None):
    """
    禁用用户(禁用用户)
    :param id:
    :return:
    """
    user = ban(User, int(id))
    if user:
        flash("禁用用户成功", "success")
        return redirect(url_for('admin.index'))


@admin.route('/users/addcompany', methods=["GET", "POST"])
def company_add():
    """
    添加企业用户
    Author: little、seven
    :return:
    """
    pass


@admin.route('/jobs/', methods=["GET", "POST"])
def jobs():
    """
    职位管理
    Author: little、seven
    :return:
    """
    page = request.args.get('page', default=1, type=int)
    pagination = Jobs.query.filter_by(deleted=0).paginate(
        page=page,
        per_page=current_app.config["ADMIN_PER_PAGE"],
        error_out=False
    )
    return render_template('admin/job_config.html', pagination=pagination)


@admin.route('/jobs/<int:id>/enable', methods=["GET", "POST"])
def job_enable(id=None):
    """
    上线职位
    Author: little、seven
    :param id:
    :return:
    """
    job = Jobs.query.get_or_404(int(id))
    if job:
        job.active = 0
        db.session.add(job)
        db.session.commit()
        flash("已经上线", "success")
        return redirect(url_for('admin.jobs'))


@admin.route('/jobs/<int:id>/disable', methods=["GET", "POST"])
def job_disable(id=None):
    """
    下线职位
    Author: little、seven
    :param id:
    :return:
    """
    job = Jobs.query.get_or_404(int(id))
    if job:
        job.active = 1
        db.session.add(job)
        db.session.commit()
        flash("已经下线", "success")
        return redirect(url_for('admin.jobs'))
