# Contributing
If you want to contribute to replpedia you need to fork this repo and change some stuff. You will need a mongob database and then when you get the url, create a enviroment variable called ``mongourl`` and set it as the url. You will also need a recaptcha token, go to [recaptcha admin](https://www.google.com/recaptcha/admin/create) and create a application with all the correct information (make sure its v2) and then create a enviroment variable called ``RECAPCTCHA`` and set it as your recaptcha secret code. 

# Tests

After you are done make sure to run the ``tests.sh`` file with bash (you need python installed) so you can make sure everything is working.