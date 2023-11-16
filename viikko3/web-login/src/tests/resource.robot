*** Settings ***
Library  SeleniumLibrary
Library  ../AppLibrary.py

*** Variables ***
${SERVER}  localhost:5001
${DELAY}  0 seconds
${HOME_URL}  http://${SERVER}
${MAIN_URL}  http://${SERVER}/ohtu
${LOGIN_URL}  http://${SERVER}/login
${REGISTER_URL}  http://${SERVER}/register

*** Keywords ***
Open And Configure Browser
   # seuraava rivi on poistettu kommenteista
    ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
    # seuraava rivi on kommentoitu
    # ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys 
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method  ${options}  add_argument  --headless
    Open Browser  browser=chrome  options=${options}
    Set Selenium Speed  ${DELAY}

Login Page Should Be Open
    Title Should Be  Login

Main Page Should Be Open
    Title Should Be  Ohtu Application main page

Welcome Page Should Be Open
    Title Should Be  Welcome to Ohtu Application!

Register Page Should Be Open
    Title Should Be  Register

Start Page Should Be Open
    Title Should Be  Ohtu Application

Go To Login Page
    Go To  ${LOGIN_URL}

Go To Register Page
    Go To  ${REGISTER_URL}

Go To Start Page
    Go To  ${HOME_URL}