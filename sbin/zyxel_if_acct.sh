#!/usr/bin/expect

# Get accounting information for interfaces
# Usage: $0 <hostname> <username> <password>

set timeout 20
set name [lindex $argv 0]
set user [lindex $argv 1]
set password [lindex $argv 2]
spawn telnet $name

expect "login:"
send "$user\n"
expect "Password:"
send "$password\n"
expect "ZySH>"
send "show interfaces accounting\n"
expect "ZySH>"
send "exit\n"
expect "ZySH>"
