from stackapi import StackAPI
from pprint import pprint
from datetime import datetime, timedelta

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
print("Our answers for the current week:")
#------ search for team answers on Stackoverflo for the current week--------
SITE = StackAPI('stackoverflow')
answers = SITE.fetch('users/{ids}/answers', ids=so_user_list)
for ans in answers['items']:
    if (ans['creation_date']) > fromdate:
        print("https://stackoverflow.com/questions/" + str(ans['answer_id']).lstrip()+" :"+ans['owner']['display_name'])
        if ans['owner']['user_id'] in so_k8s_users:
            cnt_k8s = cnt_k8s + 1
        elif ans['owner']['user_id'] in so_infra_users:
            cnt_infra = cnt_infra + 1
        elif ans['owner']['user_id'] in so_platform_users:
            cnt_platform = cnt_platform + 1
        elif ans['owner']['user_id'] in so_bigdata_users:
            cnt_bigdata = cnt_bigdata + 1
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
        if ans['owner']['user_id'] in sf_k8s_users:
            cnt_k8s = cnt_k8s + 1
        elif ans['owner']['user_id'] in sf_infra_users:
            cnt_infra = cnt_infra + 1
        elif ans['owner']['user_id'] in sf_platform_users:
            cnt_platform = cnt_platform + 1
        elif ans['owner']['user_id'] in sf_bigdata_users:
            cnt_bigdata = cnt_bigdata + 1
print("K8s:", cnt_k8s)
print("Platform:", cnt_platform)
print("Infra:", cnt_infra)
print("Bigdata:", cnt_bigdata)