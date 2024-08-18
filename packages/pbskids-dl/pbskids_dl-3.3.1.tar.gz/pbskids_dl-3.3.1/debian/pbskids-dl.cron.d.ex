#
# Regular cron jobs for the pbskids-dl package.
#
0 4	* * *	root	[ -x /usr/bin/pbskids-dl_maintenance ] && /usr/bin/pbskids-dl_maintenance
