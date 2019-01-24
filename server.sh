###################################################
# Run this script in server to keep alive the bot #
###################################################

git checkout master
git pull origin master

kill -9 `cat save_pid.txt`
rm save_pid.txt

touch bot.log
nohup python3.5 . > bot.log 2>&1 &
echo $! > save_pid.txt

tail -f bot.log
