import json
import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys

def connect_to_db():
    connection = psycopg2.connect(user= 'postgres', password = '',
                                  host = 'localhost',
                                  port= 5432,
                                  database= 'employee_db')
    return connection






12) Distribution of salaries of active employees working for more than 10 years vs 4 years vs 1 year.
    
    

def exp_mapper(x):
    if x>=10:
        return '10+ years'
    elif x >=4:
        return '4 to 10 years'
    elif x >=1:
        return '1 to 4 years'
    else:
        return 'New Joiners'
    


    connection = connect_to_db()
    
    query = """ select s.amount, date_part('year',de.to_date)- date_part('year',de.from_date) as exp 
			from employees.department_employee de join  employees.salary s 
			on s.employee_id = de.employee_id
			where date_part('year',de.to_date)- date_part('year',de.from_date) <= 60
			and date_part('year',s.to_date) = 9999;"""
                        
    df= pd.read_sql_query(query, connection)
    df['exp'] = df['exp'].astype('int')
    
    
    
    df['exp_status'] = df['exp'].apply(lambda x: exp_mapper(x))
    sns.violinplot(x= df['exp_status'], y = df['amount'])



13) Average number of years employees work in the company before leaving (title wise).
    
    
    
    connection = connect_to_db()
    
    query = """select ti.title, date_part('year',de.to_date)- date_part('year',de.from_date) as avg_yr from employees.department_employee de
				join employees.title ti on ti.employee_id = de.employee_id
				where date_part('year',de.to_date) != 9999 """
                
    df= pd.read_sql_query(query, connection)
    df['avg_yr']= df['avg_yr'].astype('int')
    df.groupby('title')['avg_yr'].mean()
    
    plot= sns.barplot(x= df['title'], y= df['avg_yr'])
    for item in plot.get_xticklabels():
        item.set_rotation(45)
        
        
        
 14) Average number of years employees work in the company before leaving (Dept wise).
    
    
    
    
       
    connection = connect_to_db()
    
    query = """select d.dept_name, date_part('year',de.to_date)- date_part('year',de.from_date) as avg_yr from employees.department_employee de
				join employees.department d on d.id = de.department_id
				where date_part('year',de.to_date) != 9999;"""
                
    df= pd.read_sql_query(query, connection)
    df['avg_yr']= df['avg_yr'].astype('int')
    df.groupby('dept_name')['avg_yr'].mean()
    
    plot= sns.barplot(x= df['dept_name'], y= df['avg_yr'])
    for item in plot.get_xticklabels():
        item.set_rotation(45)
        
        
        
        
 15) Median annual salary increment department wise
    
    
    
     connection = connect_to_db()
    query_get_all_depts= "select distinct(dept_name) from employees.department;"
    all_depts = pd.read_sql_query(query_get_all_depts, connection)['dept_name'].tolist()
    
    median_inc= {}
    for i in all_depts:
        query = """ select s.amount, d.dept_name, date_part('year', s.from_date) as start, 
                date_part('year', s.to_date) as end from employees.salary s join  employees.department_employee de 
				on s.employee_id = de.employee_id join employees.department d on d.id =de.department_id 
				where dept_name = '%s' order by s.from_date desc"""
        df = pd.read_sql_query(query %i, connection)
        df['start'] = df['start'].astype('int')
        df['end'] = df['end'].astype('int')
        my_df= df.groupby(['start'])['amount'].mean().diff()
        my_df.dropna(inplace= True)
        plot= sns.barplot(x= my_df.index, y = my_df.values)
        for item in plot.get_xticklabels():
            item.set_rotation(90)
        median_inc[i] = np.median(my_df.values)
        plt.title(i)
        plt.show()
    return median_inc






















