#!/bin/bash
#
# ----------------------------------------------------------------------------------------------------------------
# Write a script that will process the contents of /etc/shadow and output the users whose passwords are about to 
# expire (i.e., expiry date is in the following 5 days, inclusive). Assume that a user password expires when the
# expiry date is greater or equal than the current date (days since Jan 1, 1970). 
# The script should be scheduled in crontab to execute every day at 11:30 p.m and its output redirected to a file
# named “password_notices.log”.
#
# in /etc/shadow file, each line of this file contains 9 fields, separated by colons (“:”), in the following order:
#   1: login name
#   2: encrypted password
#   3: date of last password change
#   4: minimum password age
#   5: maximum password age
#   6: password warning period
#   7: password inactivity period
#   8: account expiration date
#   9: reserved field
#   
# ----------------------------------------------------------------------------------------------------------------
# Prerequisite: User who owns crontad has to have permissions do read /etc/shadow without the need to enter password
#               You may consider to enter the following line in /etc/sudoers file using "sudo visudo" command:
#               user   ALL=NOPASSWD:/bin/cat /etc/shadow
#
# CRONTAB: 30 23 * * * ~/PGSICP/PRCSE/C1/Exerc5.sh > /tmp/password_notices.log
# 
#
#
# Constant with # of days to Notice
DAYS_TO_NOTICE=5
# Calculate days since 1/1/1970. "%s" format for "date" command dives this differece in seconds. We have to divide it
# by 86400 (number of seconds in 1 day) 
days_since_beggining_of_epoch=$(( $(date +%s)/86400 ))

# AWK dould be used directly without being piped by "cat" but we have to consider security issues if we had to
# allow sudo over /etc/shadow using AWK. This way, onlu "cat" is allowed in sudoers file.
# AWK receives "DAYS_TO_NOTICE" and  "days_since_beggining_of_epoch" as variabçes to be used in notice calculation.
# ":" is the field separator (used in -F option).
# To process information, we first test if "account expiration date" is set. In other words, if field $8 has a
# length bigger than 0. If it has, we will evaluate it against the notice_period by subtracting it to current day.
# If difference is less that "notice_period" and is not in the past, than print user name (field $1)
sudo cat /etc/shadow | awk -v notice_period=$DAYS_TO_NOTICE -v today=$days_since_beggining_of_epoch -F:\
                        '{
                            if (length($8) > 0){
                                if ($8 - today <= notice_period && $8 - today > 0) print $1
                            }
                        }'

