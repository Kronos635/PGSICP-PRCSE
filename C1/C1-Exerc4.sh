#!/bin/bash
#
# Write a script that lists the top 5 “.txt” files of a given directory with the higher line count.
# The script should receive the directory as argument and perform all required validations
#
#
#
# ----------------------------------------------------------------------------------------------------------------

#Expected number of arguments
EXPECTED_ARGUMENTS=1
num_args=$#
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
            echo "Expected $EXPECTED_ARGUMENTS arguments. Found $num_args"
            ;;
    esac
}

# Main
#
# Vaidate unmber of arguments. If what expected, proceed.
if [[ $num_args -eq $EXPECTED_ARGUMENTS ]]
then
    # Fetch argument to "path" variable
    path=$1

    # test if argument is a directory
    if [ -d "$path" ]
    then
    # Count nmber of lines, excluding the "total" line produced by "wc" command as sort output numerically 
    # in reverse order. Finally, extract top 5.
    # The "awk" is a programming language by itself. It has 3 blocks: "BEGIN" (which executes at the begining),
    # BODY (an input stream that executes for each record or pattern matching), amd END (which executes once
    # at the end of stream).
    # "-F" optin specifies the field separator and -v allow us to pass a variable inside awk.
    # Inside AWK, $NF represents the number os fields.
    # In this case we just want to print the last field which corresponds to filename and 1st field that has the line
    # count.
        wc -l $path/*.txt | grep -v total | sort -n -r | head -5 |\
            awk -F/ -v path=$path 'BEGIN{
                                            print "Top 5 of txt files with more lines in \""path"\" diretory:"
                                        }
                                        {
                                            print $NF " -" $1 "Lines"
                                        }'        
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