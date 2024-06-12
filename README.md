This small project was created to collect data from Twitter via scraping techniques. Selenium was selected as the tool for the work to tackle problems like infinite scrolling built-in Twitter website.

The main part of the script is written in the twitterScraper.py file. The project consists additionally of modules for creating log files (logic stored in loggingSettings.py) and for sharing the scrape results in a .csv file with a selected e-mail address (twitterEmailSender.py). Settings file (settings.txt) was created to store various information (eg. e-mails, search and save back settings) and to enhance general reusability. The enhance portability there is a possibility to compile an .exe file of the script via pyInstaller (nessesary tweak of the file paths is added via portability.py).


0. settings.txt
Setting file (under name settings.txt in Settings folder) needs to provide following information in JSON format:
"user_agent" - user agent settings (str)
"email" - e-mail credentials for Twitter (str)
"email_password" - password credentials for the e-mail to send the results (str)
"account_name" - account name credentials for Twitter (str)
"password" - password credentials for Twitter (str)
"search_query" - subject of the searched passed to Twitter search engine (str)
"expected_screen_scrolls" - approximate number of windows to collect via script (int)
"reciever" - e-mail to which the result can be sent (str)
"log_name" - name of the log file with extension (str)
"result_name" - name of the result file with extension (str)


1. loggingSettings.py
The file stores function initialises a logger instance in other parts of the script, and a wrapper function that saves information about the steps of the execution of the script to the log file. 


2. twitterScraper.py
After loading the setting file the script initialise the logger, and creates the basic elements of the result table in the form of lists. A chromedriver instance is created with a user-agent setting (headless options are hardcoded in the function). The script attempts to enter login site, and traverse through credential entry stage, omitting the cookies window. After a successful login the script goes to the created search URL and proceeds with scraping loops fetching single tweet boxes and extracting the link, twitter handle, and the tweet itself. Fetched results are feeding the result list. The result list and the header list are passed to the prep_results function that creates a Pandas DataFrame, clears duplicates, and saves the results to a .csv file.


3. twitterEmailSender.py
The file creates a MIME object for the e-mail message to send the scraping results with a log file to the receiver's e-mail.


4. main.py twitterWork.bat
Script can be fired through either main.py file (designed for pyInstaller compilation), or through .bat file (created for Windows task scheduling).


5. portability.py
The stored there resource_path function enables creating portable .exe files via pyInstaller. Th function controls the path of the files, to enable accessing them through temporary folders created by pyInstaller, when the project is compiled. Suggested pyInstaller settings to ensure adjustments of settings and basic self-maintenance of chromedriver file:
pyinstaller main.py -w --onedir --add-data=./Settings/settings.txt:./Settings --add-data=./ChromeDriver/chromedriver.exe:./ChromeDriver --add-data=./Settings/log_file.log:./Settings --add-data=./SaveBacks/twitter.csv:./SaveBacks


Hope you'll enjoy reading the code.

Regards,
jp

jakubpoplawski@live.com
