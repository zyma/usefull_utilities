import os
import ConfigParser
import cx_Oracle
from   datetime import datetime
from   xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from   xml.dom import minidom

result_dir = "."
xslt_dir = "."

def prepare_directory():
   current_dir_name = os.path.dirname(os.path.realpath(__file__))
   current_dir_name += '/result'

   if not os.path.exists(current_dir_name):
       os.makedirs(current_dir_name)
   current_dir_name += '/' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') 
   if not os.path.exists(current_dir_name):
       os.makedirs(current_dir_name)
   else: 
       current_dir_name += '_1' 
       os.makedirs(current_dir_name)
   return current_dir_name

def get_connect(config, section):
   res = {}
   res['user'] = config.get(section, 'user')
   res['pass'] = config.get(section, 'password')
   res['db'] = config.get(section, 'db')
   return res

def get_table_info(conn, table):
   sql =  "select t.table_name, tc.table_type, tc.comments "
   sql += "from all_tables t  "
   sql += "    join all_tab_comments tc on (t.table_name = tc.table_name)  "
   sql += "where t.table_name = '" + table + "'";
   cP = conn.cursor()
   cP.execute(sql)

   res = {}
   for row in cP:
      res['TABLE_NAME'] = row[0]
      res['TABLE_TYPE'] = row[1]
      res['COMMENT'] = row[2]
   return (res)

def get_column_details(conn, table):

   sql =  "select t.column_name, t.data_type, t.data_length, t.nullable, tc.comments,  "
   sql += "       ( select (case when count(*) = 0 then 0 else 1 end ) "
   sql += "         from ALL_CONS_COLUMNS acc  "
   sql += "            join all_constraints ac on (acc.table_name = ac.table_name and constraint_type='P') "
   sql += "         where acc.column_name = t.column_name and acc.table_name = t.table_name "
   sql += "       ) as is_pk  "
   sql += "from all_tab_columns t  "
   sql += "  join all_col_comments tc on (t.column_name = tc.column_name and t.table_name = tc.table_name) "
   sql += "where t.table_name = '" + table + "' "

   cP = conn.cursor()
   cP.execute(sql)

   res = []
   for row in cP:
      dct = {}
      dct['COLUMN_NAME'] = row[0]
      dct['COLUMN_TYPE'] = row[1]
      dct['LENGTH'] = row[2]
      dct['NULLABLE'] = row[3]
      dct['COMMENTS'] = row[4]
      dct['IS_PK'] = row[5]

      res.append(dct)
   return (res)

def generate_xml(table, conn):
   table_info = get_table_info(conn, table)
   columns_info = get_column_details(conn, table)
   
   doc = minidom.Document()
   root = doc.createElement("TABLE")
   doc.appendChild(root)

   leaf = doc.createElement('TABLE_NAME')
   text = doc.createTextNode(str(table_info['TABLE_NAME']))
   leaf.appendChild(text)
   root.appendChild(leaf)

   leaf = doc.createElement('TABLE_TYPE')
   text = doc.createTextNode(str(table_info['TABLE_TYPE']))
   leaf.appendChild(text)
   root.appendChild(leaf)

   leaf = doc.createElement('COMMENT')
   text = doc.createTextNode(str(table_info['COMMENT']))
   leaf.appendChild(text)
   root.appendChild(leaf)

   leaf_columns = doc.createElement('COLUMNS')
   root.appendChild(leaf_columns)

   for col in columns_info:
      leaf_col = doc.createElement('COLUMN')
      leaf_columns.appendChild(leaf_col)

      leaf_vl = doc.createElement('COLUMN_NAME')
      text = doc.createTextNode(str(col['COLUMN_NAME']))
      leaf_vl.appendChild(text)
      leaf_col.appendChild(leaf_vl)

      leaf_vl = doc.createElement('COLUMN_TYPE')
      text = doc.createTextNode(str(col['COLUMN_TYPE']))
      leaf_vl.appendChild(text)
      leaf_col.appendChild(leaf_vl)

      leaf_vl = doc.createElement('LENGTH')
      text = doc.createTextNode(str(col['LENGTH']))
      leaf_vl.appendChild(text)
      leaf_col.appendChild(leaf_vl)

      leaf_vl = doc.createElement('NULLABLE')
      text = doc.createTextNode(str(col['NULLABLE']))
      leaf_vl.appendChild(text)
      leaf_col.appendChild(leaf_vl)

      leaf_vl = doc.createElement('COMMENTS')
      text = doc.createTextNode(str(col['COMMENTS']))
      leaf_vl.appendChild(text)
      leaf_col.appendChild(leaf_vl)

      leaf_vl = doc.createElement('IS_PK')
      text = doc.createTextNode(str(col['IS_PK']))
      leaf_vl.appendChild(text)
      leaf_col.appendChild(leaf_vl)

   xml_str = doc.toprettyxml(indent="  ")
   with open(result_dir + "/" + table + ".xml", "w") as f:
      f.write(xml_str)
   return doc

def get_xslt_list():
      from os import listdir
      from os.path import isfile

      dir_name = './XSLT'
      onlyfiles = [f for f in listdir(dir_name) if isfile(dir_name + "/" + f) and f[-4:].lower() == 'xslt']

      return onlyfiles;

def Transform(xmlRoot, xslt_file_name):
      from lxml import etree

      xslRoot = etree.fromstring(open(xslt_dir + "/" + xslt_file_name).read())
      trans = etree.XSLT(xslRoot)
      dom = etree.XML(xmlRoot.toprettyxml(indent="  "))
      transRoot = trans(dom)
      return etree.tostring(transRoot)


def run(config):
   fConnDict = get_connect(config, 'Connection')
   print 'Connection details:' + str(fConnDict)

   conn = cx_Oracle.connect(fConnDict['user']+'/' + fConnDict['pass'] + '@' + fConnDict['db'])

   tables = [x.strip() for x in config.get('Settings', 'Tables').split(',')]
   print 'Tables for loading: ' + ' '.join(tables)
   xslt_list = get_xslt_list();

   for table in tables:
      print 'Generate XML for ' + table
      xmlRoot = generate_xml(table, conn)
      print 'Transform XML for ' + table

      for xslt in xslt_list:
          print ' -- with xslt: ' + xslt
          transformed_file = Transform(xmlRoot, xslt)

          res_file_name = result_dir + "/" + table + "_" + xslt[:-5] + ".html"
          with open(res_file_name, "w") as f:
              f.write(transformed_file)
              print (' -- file ' + res_file_name + ' is saved')


print 'Start'
config = ConfigParser.SafeConfigParser()
print 'Read config'
config.read('settings.cfg')
print 'Prepare output directory'
result_dir = prepare_directory()
xslt_dir = os.path.dirname(os.path.realpath(__file__)) + "/XSLT"
run(config)

