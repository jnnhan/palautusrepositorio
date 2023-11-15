*** Settings ***
Resource  resource.robot
Test Setup  Input New Command And Create User

*** Test Cases ***
Register With Valid Username And Password
    Input Credentials  kahvikuppi  moccamaster2
    Output Should Contain  New user registered

Register With Already Taken Username And Valid Password
    TRY
        Input Credentials  kissa  haamu123
    EXCEPT  User with username kissa already exists
        Log  test succesful
    END

Register With Too Short Username And Valid Password
    Input Credentials  mo  kukkaruukku12
    Output Should Contain  Username must be at least 3 characters

Register With Enough Long But Invalid Username And Valid Password
    Input Credentials  kuppi3   matematiikka4
    Output Should Contain  Username must contain only letters a-z

Register With Valid Username And Too Short Password
    Input Credentials  krokotiili  hyppy1
    Output Should Contain  Password must be at least 8 characters

Register With Valid Username And Long Enough Password Containing Only Letters
    Input Credentials  krokotiili  hyppykeppi
    Output Should Contain  Password must not contain only letters

*** Keywords ***
Input New Command And Create User
    Input New Command
    Create User  kissa  koira123