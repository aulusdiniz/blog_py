""" Basic blog using webpy 0.3 """
import web
import model
from signals import Signals

### Url mappings
urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/login','Login'
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)

class Index:

    def GET(self):
        """ Show page """
        posts = model.get_posts()
        return render.index(posts)

class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return render.view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            size=30,
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull,
            rows=30, cols=80,
            description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content, userid='aulus')
        new_post_signal.trigger(userid='aulus') #firing the signal to new post.
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')

class Login:

    form = web.form.Form(
        web.form.Textbox('Login', web.form.notnull),
        web.form.Password('Password', web.form.notnull),
        web.form.Button('Go!'),
    )

    def GET(self):
        form = self.form
        return render.login(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.login(form)
        result = model.get_login(form.d.Login)
        if result != None:
            if result.passwd == form.d.Password:
                login_signal.trigger(userid="aulus")
                userid=form.d.Login
                raise web.seeother('/')
        else:
            return "login not found."


# the only inserted login.
model.new_login('aulus','12345')

# Declaration of signals expected.
new_post_signal = Signals(name='new_post')
login_signal = Signals(name='login')

#the user friend list.
notify_friend_dict = {  'aulus':    ['joao', 'gustavo', 'maria', 'sabrina'],
                        'joao':     ['gustavo'],
                        'maria':    ['aulus', 'sabrina']
                        }

#notify the friends when user posts new content.
def notify_friend_handler(userid):
    for item in notify_friend_dict:
        if userid == item:
            for it in notify_friend_dict[item]:
                print ('notify %s' % it)

#connecting handlers to notify when a new post comes and a new login is made.
new_post_signal.connect(notify_friend_handler)
login_signal.connect(notify_friend_handler)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
