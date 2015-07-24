# Blog-CLI
====
A command line blogging application using Cement Framework.

####DEPENDENCIES
This application uses pip, Cement 2.6.x framework,Sqlite3 and Python 3.4.x .


####INSTALLATION
Please follow the steps for installation.
- To install pip 
  ```
sudo apt-get install python3-pip
```
- To install Cement ( You can avoid this step, the application installs Cement framework)
  ```
sudo pip install cement
```
- Clone the repository and Unzip the content in a folder.
- Enter the terminal and Create a virtual Environment(Python3) for simplictiy.
- From the folder , First run the createdb.py file. (This will creeate a database for the blog to be stored)
```
python createdb.py
```
- Run the blog.py file with help arguments to view all the possible commands and options available.
```
python blog.py --help
```

####USAGE
Steps to use the application efficiently.
- The application is divided broadly into two controllers 'post' and 'category' , with each controller having seperate commands and arguments to be passed.
- To view the commands for Post , type the following command (Similarly can be done for Category)
```
python blog.py Post --help
```
- Remember it's "Post" and not "post".
- It has three commands add,list,search.
    - add =>Adds a new blog bost with blog id, blog title, blog content.
      - Uses arguments --id,--title,--content
      ```
      python blog.py Post add --id 1 --title First --content "This is my first blog"
      ```
    - list => Displays all the blog posts
      - Uses no arguments
      ```
      python blog.py Post list
      ```
    - search => Searches for a keyword in the title or content of the blog. Displays them.
      - Uses --keyword argument
      ```
      python blog.py Post search --keyword first
      ```
- Category has three commands too.
```
python blog.py Category --help
```
- Remember it's "Category" and not "category".
- It has three commands add,list,search.
    - add =>Adds a new category of blog .
      - Uses arguments --id,--category
      ```
      python blog.py Category add --id 1 --category Personal
      ```
    - list => Displays all the categories available that can be assigned to a blog post.
      - Uses no arguments
      ```
      python blog.py Category list
      ```
    - assign => Assigns the category to a blog using the <blog_id> and <cat_id>
      - Uses --postid and --id
      ```
      python blog.py Category --postid 1 --id 1
      ```
      - Remember this is the only way to assign a category to a blog , else by default it will display No Value
