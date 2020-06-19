from stackapi import StackAPI
from datetime import datetime, timedelta
import gspread
import sys

today = datetime.now()
print(today)
start = today - timedelta(days=today.weekday()+1)
end = start + timedelta(days=7)
fromdate = datetime.timestamp(start)
todate = datetime.timestamp(today)
cnt_k8s = 0
cnt_infra = 0
cnt_platform = 0
cnt_bigdata = 0
question_ids = []
answers_ids = []
valid_q = []
row = 2
week = start.strftime("%Y-%m-%d")

if len(sys.argv) < 2:
    print('Start date is not set. Default is start of the week: '+ week)
elif len(sys.argv) == 2:
    try:
        start = datetime.strptime(sys.argv[1], '%Y-%m-%d')
        # start = var_date
        fromdate = datetime.timestamp(start)
        week = 'Custom date'
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
elif len(sys.argv) == 3:
    try:
        start = datetime.strptime(sys.argv[1], '%Y-%m-%d')
        end = datetime.strptime(sys.argv[2], '%Y-%m-%d')
        fromdate = datetime.timestamp(start)
        todate = datetime.timestamp(end)
        week = 'Custom date'
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
else:
    print ('Too many parameters. Should be maximum 2: from_date, to_date')
    exit()

# Initialize Google spreadsheet with service account.
# Credentails are stored in ~/.config/gspread/service_account.json
# Instruction how to Enable API Access for a Project -
# https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project
gc = gspread.service_account()
sh = gc.open('Weekly Stack results')

# check if worksheet exists. If yes - remove and create a new one, otherwise just create a new one
try:
    wks = sh.worksheet(week)
    sh.del_worksheet(wks)
    wks = sh.add_worksheet(title=week, rows="200", cols="20")
    print('Spreadsheet ' + str(week) + ' cleared')
except:
    wks = sh.add_worksheet(title=week, rows="200", cols="20")
    print ('Spreadsheet ' + str(week) + ' not found. Created a new one')

# Set header
wks.update_cell(1, 1, 'Link')
wks.update_cell(1, 2, 'User')
wks.update_cell(1, 3, 'Shard')
wks.update_cell(1, 4, 'Is Accepted')
wks.update_cell(1, 5, 'Score')
wks.update_cell(1, 6, 'Creation Date')
wks.update_cell(1, 7, 'Last update')
wks.update_cell(1, 8, 'Script is running...')
wks.format("G1:H1", {
    "backgroundColor": {
      "red": 1.0,
      "green": 0.2,
      "blue": 0.4
    }
})
wks.format('A1:H1', {'textFormat': {'bold': True}})


so_user_list = [12857703, 7090016, 12153576, 12257134, 12767257, 12201084, 11977760, 1466573,12571387,11207414,11714114,11602913,11102471,9928809,12237732,11300382,12524159,12014434,11901958,12518487,10161306,3156333,11148139,12428794,11101419,12410332,10347794,12186585,9929015,9521610,12257250,11560878,10892354]
sf_user_list = [529478, 475392, 527253, 551540, 545593, 504596, 544933, 545585, 545145, 538661, 545622, 515276, 529873, 511418, 545600, 517692, 551964, 542573, 551980, 360872, 513968, 511923, 494031, 545721, 477518, 469845, 525879]

so_k8s_users = [12153576, 12257134, 12201084, 11977760, 1466573 ,11207414 ,11714114 ,11102471 ,12237732 ,11300382 ,12524159 ,12014434 ,11901958, 3156333 ,11148139, 11101419, 10347794, 12186585, 9929015, 9521610, 11560878]
so_infra_users = [11602913, 12428794, 12257250, 10892354]
so_bigdata_users = [7090016, 12571387, 9928809, 12518487]
so_platform_users = [12857703, 12767257, 10161306, 12410332]

sf_k8s_users = [544933, 545585, 545145, 538661, 545622, 515276, 529873, 511418, 545600, 517692, 551964, 542573, 551980, 360872, 513968, 511923, 494031, 545721, 477518, 469845, 525879]
sf_infra_users = [527253, 551540, 545593, 504596]
sf_bigdata_users = [529478, 475392]
sf_platform_users = []

tags = ['bigtable', 'editor-addons', 'gae-datastore', 'gce-persistent-disk', 'gcloud', 'gcloud-intellij', 'gcloud-java', 'gcloud-node', 'gcloud-python', 'gcsfuse', 'gcutil', 'gke-networking', 'gmail-addons', 'gmail-api', 'gmail-imap', 'gmail-promo-tab', 'google-admin-sdk', 'google-anthos', 'google-app-engine', 'google-apps-activity', 'google-apps-marketplace', 'google-apps-script', 'google-bigquery', 'google-calendar-api', 'google-cdn', 'google-chat', 'google-classroom', 'google-cloud-armor', 'google-cloud-bigtable', 'google-cloud-build', 'google-cloud-cdn', 'google-cloud-composer', 'google-cloud-data-fusion', 'google-cloud-data-transfer', 'google-cloud-dataflow', 'google-cloud-datastore', 'google-cloud-debugger', 'google-cloud-dlp', 'google-cloud-dns', 'google-cloud-dotnet', 'google-cloud-eclipse', 'google-cloud-endpoints', 'google-cloud-filestore', 'google-cloud-firestore', 'google-cloud-functions', 'google-cloud-http-load-balancer', 'google-cloud-intellij', 'google-cloud-interconnect', 'google-cloud-internal-load-balancer', 'google-cloud-kms', 'google-cloud-logging', 'google-cloud-memorystore', 'google-cloud-monitoring', 'google-cloud-network-load-balancer', 'google-cloud-networking', 'google-cloud-platform', 'google-cloud-powershell', 'google-cloud-python', 'google-cloud-router', 'google-cloud-run', 'google-cloud-scheduler', 'google-cloud-sdk', 'google-cloud-source-repos', 'google-cloud-spanner', 'google-cloud-sql', 'google-cloud-storage', 'google-cloud-talent-solution', 'google-cloud-tasks', 'google-cloud-tcp-proxy', 'google-cloud-trace', 'google-cloud-visualstudio', 'google-cloud-vpn', 'google-compute-engine', 'google-container-builder', 'google-container-os', 'google-container-registry', 'google-deployment-manager', 'google-docs', 'google-docs-api', 'google-drive-android-api', 'google-drive-api', 'google-drive-picker', 'google-drive-realtime-api', 'google-drive-sdk', 'google-eclipse-plugin', 'google-genomics', 'google-kubernetes-engine', 'google-people', 'google-people-api', 'google-persistent-disk', 'google-picker', 'google-plugin-eclipse', 'google-sheets', 'google-sheets-api', 'google-slides', 'google-slides-api', 'google-stackdriver', 'google-tasks', 'google-tasks-api', 'google-vault-api', 'google-voice', 'gsuite-addons', 'gsutil', 'hangout', 'hangouts-api', 'hangouts-chat', 'istio', 'kube-dns', 'kube-proxy', 'kubectl', 'kubelet', 'kubernetes', 'kubernetes-go-client', 'kubernetes-health-check', 'kubernetes-ingress', 'maven-gae-plugin', 'minikube', 'stackdriver', 'firebase']

print('List of answers for the date range ' + str(start) + ' - ' + str(end))


# Get all Stackoverflow answers for the date
SITE = StackAPI('stackoverflow')
answers = SITE.fetch('users/{ids}/answers', ids=so_user_list)
for ans in answers['items']:
    if (ans['creation_date']) > fromdate and (ans['creation_date']) <= todate:
        question_ids.append(ans['question_id'])

# Creat a list of questions with supported tags-----
if len(question_ids) > 0:
    question = SITE.fetch('questions/{ids}', ids=question_ids)
    for q in question['items']:
        for t in q['tags']:
                if t in tags:
                    valid_q.append(q['question_id'])
                    break
else:
    print('No answers found on Stackoverflow')

# Export to Sheets
for ans in answers['items']:
    if ans['question_id'] in valid_q:
        print("https://stackoverflow.com/questions/" + str(ans['answer_id']).lstrip()+": "+ans['owner']['display_name']+": "+str(ans['score'])+": "+str(datetime.fromtimestamp(ans['creation_date'])))
        # Insert results into spreadsheet
        wks.update_cell(row, 1, "https://stackoverflow.com/questions/" + str(ans['answer_id']))
        wks.update_cell(row, 2, ans['owner']['display_name'])
        wks.update_cell(row, 4, ans['is_accepted'])
        wks.update_cell(row, 5, ans['score'])
        wks.update_cell(row, 6, str(datetime.fromtimestamp(ans['creation_date'])))
        if ans['owner']['user_id'] in so_k8s_users:
            cnt_k8s = cnt_k8s + 1
            wks.update_cell(row, 3, 'K8s')
        elif ans['owner']['user_id'] in so_infra_users:
            cnt_infra = cnt_infra + 1
            wks.update_cell(row, 3, 'Infra')
        elif ans['owner']['user_id'] in so_platform_users:
            cnt_platform = cnt_platform + 1
            wks.update_cell(row, 3, 'Platform')
        elif ans['owner']['user_id'] in so_bigdata_users:
            cnt_bigdata = cnt_bigdata + 1
            wks.update_cell(row, 3, 'Bigdata')
        row = row + 1


# Get all Serverfault answers for the date
question_ids = []
valid_q = []
SITE = StackAPI('serverfault')
answers = SITE.fetch('users/{ids}/answers', ids=sf_user_list)
for ans in answers['items']:
    if (ans['creation_date']) > fromdate and (ans['creation_date']) <= todate:
        question_ids.append(ans['question_id'])

# Creat a list of questions with supported tags-----
if len(question_ids) > 0:
    question = SITE.fetch('questions/{ids}', ids=question_ids)
    for q in question['items']:
        for t in q['tags']:
                if t in tags:
                    valid_q.append(q['question_id'])
                    break
else:
    print('No answers found on Serverfault')

for ans in answers['items']:
    if ans['question_id'] in valid_q:
        print("https://serverfault.com/questions/" + str(ans['answer_id']).lstrip()+" :"+ans['owner']['display_name'])
        wks.update_cell(row, 1, "https://serverfault.com/questions/" + str(ans['answer_id']))
        wks.update_cell(row, 2, ans['owner']['display_name'])
        wks.update_cell(row, 4, ans['is_accepted'])
        wks.update_cell(row, 5, ans['score'])
        wks.update_cell(row, 6, str(datetime.fromtimestamp(ans['creation_date'])))
        if ans['owner']['user_id'] in sf_k8s_users:
            cnt_k8s = cnt_k8s + 1
            wks.update_cell(row, 3, 'K8s')
        elif ans['owner']['user_id'] in sf_infra_users:
            cnt_infra = cnt_infra + 1
            wks.update_cell(row, 3, 'Infra')
        elif ans['owner']['user_id'] in sf_platform_users:
            cnt_platform = cnt_platform + 1
            wks.update_cell(row, 3, 'Platform')
        elif ans['owner']['user_id'] in sf_bigdata_users:
            cnt_bigdata = cnt_bigdata + 1
            wks.update_cell(row, 3, 'Bigdata')
        row = row + 1

print("K8s:", cnt_k8s)
print("Platform:", cnt_platform)
print("Infra:", cnt_infra)
print("Bigdata:", cnt_bigdata)

wks.update_cell(3, 7, 'K8s')
wks.update_cell(3, 8, str(cnt_k8s))

wks.update_cell(4, 7, 'Platform')
wks.update_cell(4, 8, str(cnt_platform))

wks.update_cell(5, 7, 'Infra')
wks.update_cell(5, 8, str(cnt_infra))

wks.update_cell(6, 7, 'Bigdata')
wks.update_cell(6, 8, str(cnt_bigdata))

wks.update_cell(1, 8, str(today)) # set update time
