from stackapi import StackAPI
from pprint import pprint
from datetime import datetime, timedelta
import gspread

today = datetime.now()
start = today - timedelta(days=today.weekday()+1)
end = start + timedelta(days=7)
fromdate = datetime.timestamp(start)
todate = datetime.timestamp(end)
cnt_k8s = 0
cnt_infra = 0
cnt_platform = 0
cnt_bigdata = 0
question_ids = []
answers_ids = []
row = 2
week = start.strftime("%Y-%m-%d")
print(week)

#Initialize Google spreadsheet with service account. 
#Credentails are stored in ~/.config/gspread/service_account.json
#Instruction how to Enable API Access for a Project - 
#https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project
gc = gspread.service_account()
sh = gc.open('Weekly Stack results')
#check if worksheet exists. If yes - remove and create a new one, otherwise just create a new one
try:
    wks = sh.worksheet(week)
    sh.del_worksheet(wks)
    wks = sh.add_worksheet(title=week, rows="200", cols="20")
    print('Spreadsheet ' + str(week) + 'cleared')
except:
    wks = sh.add_worksheet(title=week, rows="200", cols="20")
    print ('Spreadsheet ' + str(week) + 'not found. Created new one')

# Set header
wks.update_cell(1, 1, 'Link')
wks.update_cell(1, 2, 'User')
wks.update_cell(1, 3, 'Shard')
wks.update_cell(1, 4, 'Is Accepted')
wks.update_cell(1, 5, 'Score')
wks.format('A1:F1', {'textFormat': {'bold': True}})


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

tags = ['kubernetes', 'minikube', 'istio', 'gcp', 'k8s', 'gke', 'google-kubernetes-engine', 'google-cloud-firestore', 'google-cloud-platform', 'google-compute-engine', 'google-cloud-composer', 'google-data-studio', 'google-bigquery', 'google-app-engine', 'firebase', 'kubectl', 'airflow']

print("Our answers for the current week:")
#------ search for team answers on Stackoverflow for the current week--------
SITE = StackAPI('stackoverflow')
answers = SITE.fetch('users/{ids}/answers', ids=so_user_list)
for ans in answers['items']:
    if (ans['creation_date']) > fromdate:
        print("https://stackoverflow.com/questions/" + str(ans['answer_id']).lstrip()+" :"+ans['owner']['display_name']+str(ans['score']))
        # Insert results into spreadsheet
        wks.update_cell(row, 1, "https://stackoverflow.com/questions/" + str(ans['answer_id']))
        wks.update_cell(row, 2, ans['owner']['display_name'])
        wks.update_cell(row, 4, ans['is_accepted'])
        wks.update_cell(row, 5, ans['score'])
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
#-------Check if questions contain supported tags-----
# question = SITE.fetch('questions/{ids}', ids=question_ids)
# for q in question['items']:
#     for t in q['tags']:
#         if t in tags:
#             print("ID to remove:",q['question_id'])
#             question_ids.remove(q['question_id'])

#------ search for team answers on Serferfault for the current week--------
SITE = StackAPI('serverfault')
answers = SITE.fetch('users/{ids}/answers', ids=sf_user_list)
for ans in answers['items']:    
    if (ans['creation_date']) > fromdate:
        print("https://serverfault.com/questions/" + str(ans['answer_id']).lstrip()+" :"+ans['owner']['display_name'])
        # Insert results into spreadsheet
        wks.update_cell(row, 1, "https://serverfault.com/questions/" + str(ans['answer_id']))
        wks.update_cell(row, 2, ans['owner']['display_name'])
        wks.update_cell(row, 4, ans['is_accepted'])
        wks.update_cell(row, 5, ans['score'])
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
