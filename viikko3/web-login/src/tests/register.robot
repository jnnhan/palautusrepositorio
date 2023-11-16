*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Registering Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  koodari
    Set Password  salasana22
    Set Password Confirmation  salasana22
    Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  mo
    Set Password  salasana22
    Set Password Confirmation  salasana22
    Register
    Register Should Fail With Message  Username must be at least 3 characters

Register With Valid Username And Invalid Password
    Set Username  kampela
    Set Password  kultaharkko
    Set Password Confirmation  kultaharkko
    Register
    Register Should Fail With Message  Password must not contain only letters

Register With Nonmatching Password And Password Confirmation
    Set Username  kampela
    Set Password  kultaharkko22
    Set Password Confirmation  punajuuri22
    Register
    Register Should Fail With Message  The passwords do not match

Login After Successful Registration
    Set Username  ruukkukasvi
    Set Password  punajuuri123
    Set Password Confirmation  punajuuri123
    Register
    Register Should Succeed
    Go To Login Page
    Set Username  ruukkukasvi
    Set Password  punajuuri123
    Submit Credentials
    Login Should Succeed

Login After Failed Registration
    Set Username  ru
    Set Password  punajuuri123
    Set Password Confirmation  punajuuri123
    Register
    Register Should Fail With Message  Username must be at least 3 characters
    Go To Login Page
    Set Username  ru
    Set Password  punajuuri123
    Submit Credentials
    Login Should Fail With Message  Invalid username or password

*** Keywords ***
Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}

Register Should Succeed
    Welcome Page Should Be Open

Login Should Succeed
    Main Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Register
    Click Button  Register

Submit Credentials
    Click Button  Login

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Go To Registering Page
    Go To Register Page
    Register Page Should Be Open
