
import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):
    def test_spinout_timestamp(self):
        obj = DbtPyTestFunctions()
        obj.assert_expect(self.run_test_spinout_timestamp)

    def run_test_spinout_timestamp(self):
        conn = DbtPy.connect(config.ConnStr, config.user, config.password)

        # Get the server type
        serverinfo = DbtPy.server_info( conn )

        if conn:

            drop = "DROP PROCEDURE PROC_TIMESTAMP"
            try:
                result = DbtPy.exec_immediate(conn,drop)
            except:
                pass

            # Create the SP with timestamp parameters

            
            create = "CREATE PROCEDURE PROC_TIMESTAMP ( INOUT PAR1 DATETIME YEAR TO FRACTION(5), OUT PAR2 DATETIME YEAR TO FRACTION(5)) LET PAR2 = PAR1; END PROCEDURE"
            result = DbtPy.exec_immediate(conn, create)

            # call the SP. Expect PAR2 to contain value passed to PAR1
            par1 = "2017-05-13 22:47:29.82688"
            par2 = ""

            print("Values of bound parameters _before_ CALL:")
            print("  1: %s 2: %s\n" % (par1, par2))

            stmt, par1, par2 = DbtPy.callproc(conn, 'proc_timestamp', (par1, par2))
            if stmt is not None:
                print("Values of bound parameters _after_ CALL:")
                print("  1: %s 2: %s\n" % (par1, par2))

            DbtPy.close(conn)
        else:
            print ("Connection failed.")

#__END__
#__LUW_EXPECTED__
#Values of bound parameters _before_ CALL:
#  1: 2017-05-13 22:47:29.82688 2: 
#
#Values of bound parameters _after_ CALL:
#  1: 2017-05-13 22:47:29.82688 2: 2017-05-13 22:47:29.82688

