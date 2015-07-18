from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler, hook
from cement.core.exc import FrameworkError, CaughtSignal
import sqlite3

sqlite_file = 'blog_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


class MyBaseController(CementBaseController):

    class Meta:
        label = 'base'
        description = "This application is a command line blogging application 	use the --help command to view commands available"


class Post(CementBaseController):

    class Meta:
        label = 'Post'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "This command is used to Post/List/Search blogs"
        arguments = [
            (['--id'], dict(action='store', dest='id', help='Blog ID')),
            (['--title'], dict(action='store', dest='title', help='Blog Name')),
            (['--content'], dict(action='store', dest='content', help='Blog Content')),
            (['--keyword'],
             dict(action='store', dest='keyword', help='Search Keyword'))
        ]

    @expose(help="This comman will add a new blog.")
    def add(self):
        self.app.log.info("Blog Added")
        c.execute(
            "INSERT INTO blog (blog_id,blog_title,blog_content) VALUES (" +
            self.app.pargs.id +
            ",'" +
            self.app.pargs.title +
            "','" +
            self.app.pargs.content +
            "')")
        conn.commit()

    @expose(help="This command will list all the blog posts.")
    def list(self):
        self.app.log.info("List of Blogs")
        c.execute("SELECT blog_id,blog_title,blog_content,category from blog")
        for row in c:
            print("ID = ", row[0])
            print("Title = ", row[1])
            print("Content = ", row[2])
            print("Category = ", row[3], "\n")

    @expose(help="This command will search a specific blog post.")
    def search(self):
        self.app.log.info("Search Results")
        c.execute(
            "SELECT blog_id,blog_title,blog_content,category from blog where blog_title like ('%" +
            self.app.pargs.keyword +
            "%') or blog_content like ('%" +
            self.app.pargs.keyword +
            "%');")
        for row in c:
            print("ID = ", row[0])
            print("Title = ", row[1])
            print("Content = ", row[2])
            print("Category = ", row[3], "\n")


class Category(CementBaseController):

    class Meta:
        label = 'Category'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "This command is used to add Category to the blogs"
        arguments = [
            (['--id'],
             dict(action='store', dest='id', help='Category ID')),
            (['--category'],
             dict(action='store', dest='category', help='Category Name')),
            (['--postid'],
             dict(action='store', dest='postid', help='Post ID'))
        ]

    @expose(help="This command will add a new Category.")
    def add(self):
        self.app.log.info("Category Added")
        c.execute(
            "INSERT INTO category (cat_id,category) VALUES (" +
            self.app.pargs.id +
            ",'" +
            self.app.pargs.category +
            "')")
        conn.commit()

    @expose(help="This command will list all the Category posts.")
    def list(self):
        self.app.log.info("List of Category")
        c.execute("SELECT cat_id,category from category;")
        for row in c:
            print("ID = ", row[0])
            print("Category = ", row[1], "\n")

    @expose(help="This command will assign post a new Category.")
    def assign(self):
        self.app.log.info("Category Assigned")
        c.execute(
            "UPDATE blog SET category=(Select category from category where " +
            self.app.pargs.postid +
            "= blog.blog_id and category.cat_id =" +
            self.app.pargs.id +
            ") where exists( select * from category where " +
            self.app.pargs.postid +
            "= blog.blog_id and category.cat_id =" +
            self.app.pargs.id +
            ");")
        conn.commit()


def my_cleanup():
    conn.close()


class MyApp(CementApp):

    class Meta:
        label = 'myapp'
        base_controller = 'base'
        handlers = [MyBaseController, Post, Category]
        hook.register('pre_close', my_cleanup)


def main():
    with MyApp() as app:
        try:
            app.run()
        except FrameworkError as e:
            print("Framework Error => %s " % e)
        finally:
            app.close()

if __name__ == '__main__':
    main()
