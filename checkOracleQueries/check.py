import os
import csv
import ConfigParser
import cx_Oracle
from datetime import datetime


def get_connect(config, section):
   res = {}
   res['user'] = config.get(section, 'user')
   res['pass'] = config.get(section, 'password')
   res['db'] = config.get(section, 'db')
   return res
	

def get_query(file_name):
   file = open(file_name, 'r')
   sql = file.read()
   file.close()
   return sql


def set_statistics_level(conn): 
   pre_query = 'ALTER SESSION SET STATISTICS_LEVEL=ALL'
   cP = conn.cursor()
   cP.execute(pre_query)

def save_execution_plan(conn, out_put_file):
   perf_sql = "SELECT * FROM TABLE (DBMS_XPLAN.display_cursor (format => 'ALL IOSTATS MEMSTATS LAST'))";
   cP = conn.cursor()
   cP.execute(perf_sql)
   out_put_file.write('\n')
   out_put_file.write('\n')
   for row in cP:
      out_put_file.write(str(row[0])  + '\n');

def save_ds_to_file(output_file_name, cursor):
   col_lst = []

   for col in  cursor.description:
       col_lst.append(col[0])

   with open(output_file_name, 'wb') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(col_lst)
      for row in cursor:
          writer.writerow(row)

def run_query(connection, query, out_dir_name, seq_number, bind_vals):
   f = open(out_dir_name + '/run_tuime_data.txt',"a") 
   
   f.write("Query Num: " + str(seq_number) +'\n')
   f.write("Query: " + str(query) +'\n')
   
   conn = cx_Oracle.connect(connection['user']+'/' + connection['pass'] + '@' + connection['db'])

   set_statistics_level(conn)

   dt = datetime.now()
   f.write("Start time: " + dt.strftime('%Y.%m.%d %H:%M:%S.%f')  +'\n')

   c = conn.cursor()
   c.execute(query, bind_vals)

   dtE = datetime.now()
   f.write("Execution time  " + str(dtE - dt) + '\n')

   output_file_name = out_dir_name + '/output' + str(seq_number) + '.csv'

   save_ds_to_file(output_file_name, c);
   
   dtF = datetime.now()
   f.write("Fetch and save to file time: " + str(dtF - dtE) +'\n')
   f.write("Summary: " + str(dtF - dt) + '\n')

   save_execution_plan(conn, f)

   conn.close()
   dtEnd = datetime.now()
   f.write('Whole duration: ' + str(dtEnd - dt)  + '\n');
   f.write("End time: " + dtEnd.strftime('%Y.%m.%d %H:%M:%S.%f')  + '\n')
   f.write("====== END ======"+'\n')
   f.write("================="+'\n')
   f.write('\n')
   f.write('\n')
   f.close()


def prepare_directory():
   current_dir_name = os.path.dirname(os.path.realpath(__file__))
   current_dir_name += '/input'

   if not os.path.exists(current_dir_name):
       os.makedirs(current_dir_name)
   current_dir_name += '/' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
   if not os.path.exists(current_dir_name):
       os.makedirs(current_dir_name)
   else: 
       current_dir_name += '_1' 
       os.makedirs(current_dir_name)
   return current_dir_name


def run (seq_number, config, out_dir_name):
   fileName = 'sql_' +  str(seq_number) + '.sql'
   sectionName = str(seq_number) + '_query_connect'

   fConnDict = get_connect(config, sectionName)
   print 'Query connection details: '
   print fConnDict

   query = get_query(fileName)

   bind_vals = {}
   items = config.items(str(seq_number) + '_query_args')
   for k, v in items:
      bind_vals[k] = v

   print 'Query for running' 
   print query

   run_query(fConnDict, query, out_dir_name, seq_number, bind_vals)


config = ConfigParser.SafeConfigParser()
config.read('check.cfg')
out_dir_name = prepare_directory();

run(1, config, out_dir_name)
run(2, config, out_dir_name)

