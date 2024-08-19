# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_201_MultipleRsltsetsDiffColDefs(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_201)

  def run_test_201(self):
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
    
    serverinfo = DbtPy.server_info( conn )
    server = serverinfo.DBMS_NAME[0:3]
	
    procedure = """CREATE FUNCTION multiResults ()
       RETURNING CHAR(16), INT, VARCHAR(32), NUMERIC(7,2);
       
       DEFINE p_name CHAR(16);
       DEFINE p_id INT;
       DEFINE p_breed VARCHAR(32);
       DEFINE p_weight NUMERIC(7,2);
       
       FOREACH c1 FOR
    	  SELECT name, id, breed, weight
    	  INTO p_name, p_id, p_breed, p_weight
    	  FROM animals
    	  ORDER BY name DESC
    	  RETURN p_name, p_id, p_breed, p_weight WITH RESUME;
       END FOREACH;
    
    END FUNCTION;"""
    
    if conn:
        try:
            DbtPy.exec_immediate(conn, 'DROP PROCEDURE multiResults')
        except:
            pass
        DbtPy.exec_immediate(conn, procedure)
        stmt = DbtPy.exec_immediate(conn, 'CALL multiResults()')
    
        print("Fetching first result set")
        row = DbtPy.fetch_tuple(stmt)
        while ( row ):
           for i in row:
                print(str(i).strip())
           row = DbtPy.fetch_tuple(stmt)
       
        DbtPy.close(conn)
    else:
       print("Connection failed.")

#__END__
#__IDS_EXPECTED__
#Fetching first result set
#Sweater
#6
#llama
#150.00
#Smarty
#2
#horse
#350.00
#Rickety Ride
#5
#goat
#9.70
#Pook
#0
#cat
#3.20
#Peaches
#1
#dog
#12.30
#Gizmo
#4
#budgerigar
#0.20
#Bubbles
#3
#gold fish
#0.10
