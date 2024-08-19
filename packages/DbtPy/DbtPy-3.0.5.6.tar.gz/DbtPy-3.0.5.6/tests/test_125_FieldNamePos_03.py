# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_125_FieldNamePos_03(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_125)

  def run_test_125(self):
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
    server = DbtPy.server_info( conn )

    result = DbtPy.exec_immediate(conn, "SELECT * FROM sales")
    result2 = DbtPy.exec_immediate(conn, "SELECT * FROM staff")
    
    for i in range(0, DbtPy.num_fields(result)):
      print("%d:%s" % (i, DbtPy.field_name(result,i)))
    
    print("-----")
    
    for i in range(0, DbtPy.num_fields(result2)):
      print("%d:%s" % (i, DbtPy.field_name(result2,i)))
    
    print("-----")
    
    if (server.DBMS_NAME[0:3] == 'Inf'):
      print("Region:%s" % DbtPy.field_name(result, 'region'))
    else:
      print("Region:%s" % DbtPy.field_name(result, 'REGION'))
    print("5:%s" % DbtPy.field_name(result2, 5))

#__END__
#__LUW_EXPECTED__
#0:SALES_DATE
#1:SALES_PERSON
#2:REGION
#3:SALES
#
#-----
#0:ID
#1:NAME
#2:DEPT
#3:JOB
#4:YEARS
#5:SALARY
#6:COMM
#
#-----
#Region:REGION
#5:SALARY
#__ZOS_EXPECTED__
#0:SALES_DATE
#1:SALES_PERSON
#2:REGION
#3:SALES
#
#-----
#0:ID
#1:NAME
#2:DEPT
#3:JOB
#4:YEARS
#5:SALARY
#6:COMM
#
#-----
#Region:REGION
#5:SALARY
#__SYSTEMI_EXPECTED__
#0:SALES_DATE
#1:SALES_PERSON
#2:REGION
#3:SALES
#
#-----
#0:ID
#1:NAME
#2:DEPT
#3:JOB
#4:YEARS
#5:SALARY
#6:COMM
#
#-----
#Region:REGION
#5:SALARY
#__IDS_EXPECTED__
#0:sales_date
#1:sales_person
#2:region
#3:sales
#
#-----
#0:id
#1:name
#2:dept
#3:job
#4:years
#5:salary
#6:comm
#
#-----
#Region:region
#5:salary
