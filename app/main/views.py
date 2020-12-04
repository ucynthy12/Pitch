from flask import render_template,redirect,request,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User, Pitch ,Comment , Upvote , Downvote
from .forms import UpdateProfile , PitchForm , CommentForm,UpdateProfile
from .. import db,photos

@main.route('/')
def index():
    title = ' Home - welcome to the pitch app'
    return render_template('index.html', title = title)
@main.route('/pitch',methods=['GET','POST'])
@login_required
def pitch():
    '''
    view pitch function that returns pitch categories
    '''

    pitches =Pitch.query.all()
    product= Pitch.query.filter_by(category='Product').all()
    company= Pitch.query.filter_by(category='Company').all()
    jobs= Pitch.query.filter_by(category='Jobs').all()
    entertainment= Pitch.query.filter_by(category='Entertainment').all()

    likes= Upvote.query.all()
    dislike= Downvote.query.all()
    return render_template('pitch.html',pitches = pitches,product= product,jobs = jobs , company = company ,entertainment=entertainment, likes = likes, dislike = dislike )


@main.route('/new_picth', methods = ['POST','GET'])
@login_required
def new_pitch():

    form = PitchForm()
    if form.validate_on_submit():
        new_pitch = Pitch(title = form.title.data, post = form.post.data, category = form.category.data,user_id=current_user._get_current_object().id)
        new_pitch.save_pitch()
        return redirect(url_for('main.pitch'))
        
    return render_template('new_pitch.html', form = form)

@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    user = current_user.username
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('comment.html', form =form, pitch = pitch,comments=comments)


@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id
    posts = Pitch.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)


@main.route('/user/<name>/updateprofilepic',methods= ['POST','GET'])
@login_required
def update_profile_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile',name=name))
    return render_template('profile/updatepic.html')

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save_up()
    return redirect(url_for('main.pitch',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):

    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save_down()
    return redirect(url_for('main.pitch',id = id))
