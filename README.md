# Installation Instructions:
## Dependencies
### Python
1. Go to http://www.python.org/download/releases/2.7.5/
2. Click the second to last download link
3. Follow the instructions in the install package

### Xcode
1. Go to https://developer.apple.com/xcode/ and click the link to go to the app store
2.Download the app
3. Open Xcode, then go to Preferences --> Downloads and install the 'Command Line Tools'


### Homebrew
1. Have XCode installed
2. Go to terminal
3. Type: ```ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"```
4. Press enter when prompted

### Django
1. Go to https://www.djangoproject.com/download/ and download the tar.gz file 
2. Unzip the file, go to Terminal, and enter the made Django folder 
3. Type: ```sudo python setup.py install```

### MySQL
1. Have Homebrew installed
2. Go to terminal and type in ```brew install mysql```
3. Type: ```unset TMPDIR```
4. Type: ```mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp```
5. Type: ```sudo mv /usr/local/opt/mysql/my-new.cnf /usr/local/opt/mysql/my.cnf```
6. Type: ```cp `brew --prefix mysql`/homebrew.mxcl.mysql.plist ~/Library/LaunchAgents/```
7. Type: ```launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist```

### MySQLdb
1. Have XCode installed
2. Go to http://sourceforge.net/projects/mysql-python/?source=dlp
3. Download and unzip the file
4. Enter the newly made folder in terminal
5. Type: ```sudo python setup.py install```

## Creating an SQL table
In terminal, type the following:
  ```mysql -u root```
  ```CREATE DATABASE ula CHARACTER SET utf8;```
  ```GRANT ALL ON ula.* TO 'djangouser'@'localhost' IDENTIFIED BY 'abc123';```
  ```quit```
  
## Changing project settings
1. Go into apps/settings.py
2. Change ROOT_HTTP to /absolute/path/to/oola/folder/oola
3. In array databases settings, change 'NAME', 'USER', and 'PASSWORD' to the database information that you created
4. Type python manage.py syncdb to build database tables
5. Type python manage.py runserver to run project
6. Go to url 127.0.0.1:8000 to view the website
