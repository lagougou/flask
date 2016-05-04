from ..models import Post,Permission
from ..import db,auth
from flask import g,request,jsonify,current_app,url_for
from . import api
from .decorators import permisson_required
from .errors import forbidden



@api.route('/posts/',methods=['POST'])
def new_post():
    post=Post.from_json(request.json)
    post.author=g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()),201,\
           {'Location': url_for('api.get_post', id=post.id, _external=True)}

@api.route('/posts/')
def get_posts():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.paginate(page,per_page=current_app.config['FLASJKY_POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items
    prev=None
    if pagination.has_prev:
        prev=url_for('api.get_posts',page=page-1,_external=True)
    next=None
    if pagination.has_next:
        next=url_for('api.get_posts',page=page+1,_external=True)
    return jsonify({'posts':[post.to_json() for post in posts],
                    'prev':prev,
                    'next':next,
                    'count':pagination.total})

@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

@api.route('/posts/<int:id>', methods=['PUT'])
@permisson_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())



