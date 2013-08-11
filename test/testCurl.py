import os

os.system('''curl -d "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=qr2434061@gmail.com&Passwd=theoldreader789456&output=json" https://theoldreader.com/accounts/ClientLogin''')

res=os.popen('''curl -d "client=YourAppName&accountType=HOSTED_OR_GOOGLE&service=reader&Email=qr2434061@gmail.com&Passwd=theoldreader789456&output=json" https://theoldreader.com/accounts/ClientLogin''').read()

print "res is " + res
