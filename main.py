from string import Template
import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import time
from random import randint
import json
import difflib
import os
import shutil
import glob


# get target names
def get_targets(filename):
    names = []
    with open(filename, mode='r', encoding='utf-8') as targets_file:
        for a_target in targets_file:
            names.append(a_target.split()[0])
    return names

# Read contacts from a given file and return a
# list of names and email addresses
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

# Read message template
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def genScope(names):
    i = 0
    # loop over targets and get scope
    for name in names:
        # place target in body
        body['variables']['handle'] = names[i]

        # create/open file
        filename = './tmp/{0}'.format(names[i])
        f = open(filename, 'a')

        # make request and process relevant parts of response
        r = requests.post('https://hackerone.com/graphql', headers=headers, json=body)
        r = r.json()
        scope = r['data']['team']['in_scope_assets']['edges']
        for node in scope:
            f.write(node['node']['asset_identifier'])
            f.write('\n')
            f.write(node['node']['instruction'])
        i += 1
        f.close
        time.sleep(randint(3,5))

if __name__ == "__main__":

    # create diff signal & details
    global diff, details
    diff = False
    details = ''

    # get request headers
    with open('./requests/headers.json') as f:
        headers = json.load(f)

    # get request body
    with open('./requests/body') as f:
        body = json.load(f)
    
    names = get_targets('targets.txt')

    # generate current scope
    genScope(names)

    # diff previous and current scope
    for i in range(len(names)):
        # prepare previous scope for diff
        filename = './responses/{0}'.format(names[i])
        old = open(filename, 'r')
        oldL = old.readlines()
        old.close

        # prepare current scope for diff
        filename2 = './tmp/{0}'.format(names[i])
        new = open(filename2, 'r')
        newL = new.readlines()
        new.close

        # add link
        details += '\nLink: https://hackerone.com/{0}?type=team\n\n'.format(names[i])
        # perform diff
        for line in difflib.context_diff(oldL, newL, fromfile='{0}_old'.format(names[i]), tofile='{0}_new'.format(names[i])):
            
            # append diff to details
            details+=str(line)

            # signal diff
            diff = True
        details += '\n'
    
    if diff != True:
        files = glob.glob('./tmp/*')
        
        # remove temp files
        for file in files:
            os.remove(file)

    if diff == True:
        # import creds
        creds = yaml.load(open('./secrets.yml'), Loader=yaml.FullLoader)
    
        # set up the SMTP server
        s = smtplib.SMTP(host=creds['smtp_host'], port=587)
        s.ehlo()
        s.starttls()
        s.login(creds['mail'], creds['mail_pass'])

        names, emails = get_contacts('contacts.txt')  # read contacts
        message_template = read_template('message.txt')

        # For each contact, send the email:
        for name, email in zip(names, emails):
            msg = MIMEMultipart()       # create a message

            # add recipient name to the message template
            message = message_template.substitute(NAME=name.title(), DETAILS=details)

            # setup the parameters of the message
            msg['From']=creds['mail']
            msg['To']=email
            msg['Subject']="HackerOne Scope Change"

            # add the message body
            msg.attach(MIMEText(message, 'plain'))

            # send
            s.send_message(msg)
    
            del msg
        
        # replace old check files
        cwd = os.getcwd() 
        src = cwd + '/tmp/'
        dst = cwd + '/responses/'

        files = glob.glob(src + '*')
        targets = os.listdir('./tmp')
        i = 0
        for file in files:
            shutil.move(os.path.join(src, file), os.path.join(dst, targets[i]))
            i+=1