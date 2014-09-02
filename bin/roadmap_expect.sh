#!/usr/bin/expect
set timeout 11000
log_file -noappend roadmap_sync.log;
spawn ./roadmap_update.sh 
expect "JIRA password (roadmap-sync):" 
send ""
expect eof
exit
