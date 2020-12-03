from flask_wtf import FlaskForm
from wtforms import StringField, SelectField , TextAreaField , SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write something about you.',validators=[Required()])
    submit = SubmitField('Save')

class PitchForm(FlaskForm):
    title = StringField('Title',validators =[Required()])
    category = SelectField('Category', choices =[('Product','Product'),('Jobs','Jobs'),('Company','Company'),('Entertainment','Entertainment')])
    post = TextAreaField('Pitch',validators =[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Share your comment',validators =[Required()])
    submit = SubmitField('comment')

