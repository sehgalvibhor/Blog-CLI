import sqlite3
import os
import sys
import importlib
import site

def insimport(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print("Installing module")
        import pip
        if hasattr(sys,'real_prefix'):
            pip.main(['install', package])
        else:
            pip.main(['install','--user', package])
            importlib.reload(site)

        
insimport('cement')

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler, hook
from cement.core.exc import FrameworkError


sqlite_file = 'blog_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

class Error(Exception):
    pass

class MissingArgs(Error):
    pass

class EmptyData(Error):
    pass

class MyBaseController(CementBaseController):

    class Meta:
        label = 'base'
        description = "This application is a command line blogging application "

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])
    
class Post(CementBaseController):

    class Meta:
        label = 'Post'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "This command is used to Post/List/Search blogs"
        arguments = [
            (['--id'], dict(action='store',dest='id', help='Blog ID')),
            (['--title'], dict(action='store', dest='title', help='Blog Name')),
            (['--content'], dict(action='store', dest='content', help='Blog Content')),
            (['--keyword'],
             dict(action='store', dest='keyword', help='Search Keyword'))
        ]

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])
    
    @expose(help="This command will add a new blog.")
    def add(self):
        try:
            if self.app.pargs.id==None or self.app.pargs.title==None or self.app.pargs.content ==None:
                raise MissingArgs
            else:
                c.execute(
                "INSERT INTO blog (blog_id,blog_title,blog_content) VALUES (?,?,?)",(self.app.pargs.id,self.app.pargs.title,self.app.pargs.content ))
                conn.commit()
                self.app.log.info("Blog Added")
        except MissingArgs:
            print("Arguments required were missing, Add all the arguments")
        except Exception as e:
            print ("Error ",e)
        finally:
            conn.rollback()

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
        try:
            if self.app.pargs.keyword==None:
                raise MissingArgs
            else:
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
        except MissingArgs:
            print("Arguments required were missing, Add all the arguments")
        except Exception as e:
            print ("Error ",e)


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

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])
    

    @expose(help="This command will add a new Category.")
    def add(self):
        try:
            if self.app.pargs.id==None or self.app.pargs.category==None:
                raise MissingArgs
            else:
                c.execute(
                    "INSERT INTO category (cat_id,category) VALUES (" +
                    self.app.pargs.id +
                    ",'" +
                    self.app.pargs.category +
                    "')")
                conn.commit()
                self.app.log.info("Category Added")
        except MissingArgs:
            print("Arguments required were missing, Add all the arguments")
        except Exception as e:
            print ("Error ",e)
                

    @expose(help="This command will list all the Category posts.")
    def list(self):
        c.execute("SELECT cat_id,category from category;")
        try: 
            self.app.log.info("List of Category")
            for row in c:
                print("ID = ", row[0])
                print("Category = ", row[1], "\n")
        except Exception as e:
            print("Error",e)

    @expose(help="This command will assign post a new Category.")
    def assign(self):
        try:
            c.execute("Select count(cat_id) from category where cat_id =="+self.app.pargs.id )
            for row in c:
                x= (int(row[0]))       
            c.execute("Select count(blog_id) from blog where blog_id =="+self.app.pargs.postid )
            for row1 in c:
                y= (int(row1[0]))
            if self.app.pargs.postid ==None or self.app.pargs.id==None :
                raise MissingArgs    
            elif x==0 or y==0:
                raise EmptyData
            else:    
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
                self.app.log.info("Category Assigned")
        except EmptyData:
            print(" Either the id of blog or category doesnot exist")
        except MissingArgs:
            print("Arguments required were missing, Add all the arguments")
        except Exception as e:
            print ("Error",e)


def my_cleanup():
    conn.close()


class MyApp(CementApp):

    class Meta:
        label = 'myapp'
        base_controller = 'base'
        handlers = [MyBaseController, Post, Category]
        hook.register('pre_close', my_cleanup)


def main():
    app=MyApp()
    app.setup()
    try:
        app.run()
    except FrameworkError as e:
        print("Framework Error => %s " % e)
    finally:
        app.close()

if __name__ == '__main__':
    main()
