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
    Submit Credentials
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  mo
    Set Password  salasana22
    Set Password Confirmation  salasana22
    Submit Credentials
    Register Should Fail With Message  Username must be at least 3 characters

Register With Valid Username And Invalid Password
    Set Username  kampela
    Set Password  kultaharkko
    Set Password Confirmation  kultaharkko
    Submit Credentials
    Register Should Fail With Message  Password must not contain only letters

Register With Nonmatching Password And Password Confirmation
    Set Username  kampela
    Set Password  kultaharkko22
    Set Password Confirmation  punajuuri22
    Submit Credentials
    Register Should Fail With Message  The passwords do not match

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}
    
Submit Credentials
    Click Button  Register

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
