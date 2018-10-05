# Order-Scraper

### Instructions:
1. Virtual Environment Setup:
  * Need to set up a virtual environment in python3
  * Need to install the dependencies to run this project (pip install -r requirements.txt), fortunately they have been included in the requirements.txt file
  * Need to install the gecko driver otherwise selenium won't be able to bring up the firefox engine on which the project will be mainly using.

2. Environment Variables:
  * In order to use this program, the selenium web driver will be emulating the user point of view. This means you **WILL BE PROMPTED TO LOG INTO FACEBOOK**.
  * You can do that with the help of environment variables, in which case I have used two of them, one of the email and the other for password.
  * In order to set up the environment variables in a linux machine you can do this in your console:
    * export EMAIL = <your facebook email>
    * export PASSWORD = <your facebook password>
  * After that you're done and after that you can proceed to step 3 if it applies to you, if not go directly to step 4.

3. Extra layer of security:
  * In most cases people have an extra layer of security associated with their facebook account. FOr my case it's the google authenticator for which reason I have written an extra line of code.
  `two_factor_bypass(driver=driver, key="278588")`
  * This calls a function that takes care of the extra layer of authenticator security that I have associated with my account. If yours is different then I suggest you chage the code to suit your needs. If it's the same then perfect. Just replace the key inside the function with your appropriate google authenticator key and it should work just fine. if you have no authentication enabled and can log into to facebook directly then you can comment out this line of code like this `# two_factor_bypass(driver=driver, key="278588")`.
  * After this we can proceed to step 4.

4. Running the program:
  * Runs just like any other python programs, just write: `python group_scrape.py` and if it works then you will have a decent output in your command line as well as an Excel file autogenerated after it's all said and done.
  * This program was run previously and the generated Excel file has been attached for reference.
  * For those who might think I made that Excel file by hand I assure you I rarely have that much free time. :P.

# Thank You.
