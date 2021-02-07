import pandas as pd
import random
import numpy as np
from flask import Flask,request,render_template

random.seed(123)
app = Flask(__name__)

users_df = pd.DataFrame(columns=['User ID', 'Class ID', 'Class Name', 'Rating'])

file = open('course_names.txt', 'r')
course_names = []
for line in file.readlines():
    if(line and 'CATEGORY' not in line):
        course_name = line.strip()
        while(True):
            try:
                _ = int(course_name[-1])
                course_name = course_name.replace(course_name[-1], '')
            except:
                course_names.append(course_name.strip())
                break
        
course_names

user_ids = list(range(175))
class_ids = list(range(175))

for user_id in user_ids:
    for class_id in class_ids:
        if_rating = random.randint(0, 1)
        if(if_rating):
            rating = random.randint(1, 10)
        else:
            rating = 0
        series = [user_id, class_id, course_names[class_id], rating]
        users_df.loc[len(users_df)] = series
        

def create_user_item_matrix(df):
    user_item = users_df.groupby(['User ID', 'Class ID'])['Rating'].unique().unstack()
    
    #to convert list to integer ratings
    for i in range(175):
        for j in range(175):
            user_item[i][j] = user_item[i][j][0]
    
    return user_item # return the user_item matrix 

user_item = create_user_item_matrix(users_df)


def get_classes_attended_by_user(user_id, df):
    attended_df = df[(df['User ID'] == user_id) & (df['Rating'] != 0)]
    return list(attended_df.sort_values(by='Rating', ascending=False)['Class ID'])


def get_similar_users(user_id, df):
    similar_users = user_item.dot(user_item[user_item.index == user_id].T)
    user_interactions  = users_df[users_df['Rating'] != 0].groupby('User ID', sort=False).count()['Class ID']
    neighbors_df = pd.merge(similar_users, user_interactions, how='left', left_index=True, right_index=True)
    neighbors_df = neighbors_df.reset_index()
    neighbors_df.columns = ['neighbor_id', 'similarity','interactions']
    neighbors_df = neighbors_df.sort_values(['similarity','interactions'],ascending=False)
    
    return neighbors_df


def get_class_titles(class_ids):
    return [course_names[int(i)] for i in class_ids]

def user_recs(user_id, n_recs=10):
  
    recs = []
    neighbors_df = get_similar_users(user_id, users_df)
    neighbor_user_ids = neighbors_df['neighbor_id'].values
    classes_attended_user = get_classes_attended_by_user(user_id, users_df)
    for neighbor_id in neighbor_user_ids:
        classes_attended_other = get_classes_attended_by_user(neighbor_id, users_df)
        new_recs = np.setdiff1d(classes_attended_other, classes_attended_user)
        recs = np.unique(np.concatenate([new_recs, recs], axis=0))
        # If we have enough recommendations exit the loop
        if len(recs) > n_recs-1:
            recs = recs[:n_recs]
            break
            
            
            
    return get_class_titles(recs)


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form.get("userID")
        n_recs = request.form.get("nRecs")
        recommendations = user_recs(int(user_id), int(n_recs))

        return render_template("index.html", recommendations=recommendations)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port=80)
