import subprocess

# generate list
p = subprocess.Popen(["python","today_cause_list.py"], stdout=subprocess.PIPE)
out,_ = p.communicate()

body = out.decode()

print("\n---- EMAIL BODY ----\n")
print(body)
print("\n--------------------\n")

# plug this body into your existing send_email() in notifier_v2.py
