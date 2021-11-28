#!/bin/bash
#
# Write a script that outputs to the screen all files of a given directory which “Other’s” have write permission.
# The script should receive the directory as argument and perform all required validations
#
#
#
# ----------------------------------------------------------------------------------------------------------------

#Expected number of arguments
EXPECTED_ARGUMENTS=1

# Function to print syntax to help user in case of error
#   Paraneters: None
#   Return: None
function need_help() {
    echo "Syntax: Exerc1.sh <path to inspect>"
}

# Function to print error context to user
#   Paraneters: $1 - parameter value
#               $2 - Error Code
#   Return: None
#   Error Codes: 1 - Invalid path
#                2 - Invalid number of Arguments
function something_is_wrong() {
    # print information to user, accordingly to kind of error
    case $2 in
        1)
            echo "\"$path\" is not a directory or it doesn't exists"
            ;;
        2)
            echo "Expected $EXPECTED_ARGUMENTS arguments. Found $#"
            ;;
    esac
}

# Main
#
# Vaidate unmber of arguments. If what expected, proceed.
if [[ $# -eq $EXPECTED_ARGUMENTS ]]
then
    # Fetch argument to "path" variable
    path=$1

    # test if argument is a directory
    if [ -d "$path" ]
    then
        # Fetch files from path
        files=($(ls "$path"))
        # loop through files and validade conditions: has write permission to "Others"?
        for file in ${files[@]}
        do
            # Fetch file permissions of file under analysis in human readable form: "rwxrwxrwx"
            permissions=`stat --printf="%A" $file`
            # Last 3 characters represent others permissions. Lets print it if it has write allowed and it s a file.
            if [[ "${permissions:(-3)}" =~ "w" && -f $file ]]
            then
                printf "\"$file\" file has write permissions to Others\n"
            fi
        done
    else
        # function calls to send information to users
        something_is_wrong "$path" "1"
        need_help
    fi
else
    # function calls to send information to users
    something_is_wrong "$path" "2"
    need_help
fi
