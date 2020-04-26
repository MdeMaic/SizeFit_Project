from flask import Blueprint, render_template, request

bp = Blueprint(
    __name__,
    __name__,
    template_folder='templates',
    url_prefix='/'
)

@bp.route('/')
def hello():
    return render_template('new_page.html')

@bp.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        return 'it works'
    return render_template('edit_page.html')