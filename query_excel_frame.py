#-*- coding: utf-8 -*-
import xlsxwriter
import pymysql
conn = pymysql.connect(
    host='127.0.0.1',
    user='edxapp001',
    password='password',
    db='edxapp',
    charset='utf8'
)
curs = conn.cursor()
sql = '''
select org, display_name, short_description, teacher_name, t2.detail_name, t3.detail_name, total, status, enrollment_start, enrollment_end, start, end
from (
select
    concat(org,' (',c.detail_name,' )') as org,
    display_name,
    short_description,
    teacher_name,
    classfy,
    middle_classfy,
    SUBSTRING(SUBSTRING_INDEX(effort, "#", 1), POSITION("@" IN effort)+1,5) as total,
    case
    when now() >= end and b.audit_yn = 'Y'
    then 'audit'
    when start <= now() and now() <= end
    then 'ing'
    when enrollment_start > now()
    then 'ready'
    else 'unknown'
    end as status,
    enrollment_start,
    enrollment_end,
    start,
    end
from course_overviews_courseoverview a
join course_overview_addinfo b
on a.id = b.course_id
left join code_detail c
on a.org = c.detail_code
where c.group_code = '003'
) t1
left join (
  select detail_code, detail_name
  from code_detail
  where group_code = '001'
) t2
on t1.classfy = t2.detail_code
left join (
  select detail_code, detail_name
  from code_detail
  where group_code = '002'
) t3
on t1.middle_classfy = t3.detail_code
where status <> 'unknown';
'''
curs.execute(sql)
rows = curs.fetchall()
conn.close()
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

idx = 1
for row in rows:
    worksheet.write('A' + str(idx), row[0])
    worksheet.write('B' + str(idx), row[1])
    worksheet.write('C' + str(idx), row[2])
    worksheet.write('D' + str(idx), row[3])
    worksheet.write('E' + str(idx), row[4])
    worksheet.write('F' + str(idx), row[5])
    worksheet.write('G' + str(idx), row[6])
    worksheet.write('H' + str(idx), row[7])
    worksheet.write('I' + str(idx), row[8])
    worksheet.write('J' + str(idx), row[9])
    worksheet.write('K' + str(idx), row[10])
    worksheet.write('L' + str(idx), row[11])
    idx += 1

workbook.close()
