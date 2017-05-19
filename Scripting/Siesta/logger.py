"""
Logger: Write out MD quantities in ASCII format ready to
be converted to Siesta MD format
1st version: just a function

Each record is marked by a single initial string (no whitespace)

The LOG file produced can be processed by the log2MD.sh script

Unstructured magnitudes can be written using the "printf" construction
and the "general object" formatter (see example below).

"""
def logger(f, step, xa,va,thermostat=None):

    # f is a file handle, which must have been opened by the caller
    
    na = len(xa[:,0])

    # na is included to help the conversion programs
    f.write( "--MDstep %10i  %7i\n" %  (step, na) )

    format = "--MDixv %7i %14.7f %14.7f %14.7f %14.7f %14.7f %14.7f\n"
    for i in range(na):
        f.write( format %  (i+1, xa[i,0],xa[i,1],xa[i,2], va[i,0],va[i,1],va[i,2]) )

    # Thermostat must be in the form (s,vs)
    if thermostat is not None:  
        f.write("--MDthermostat  %14.7f %14.7f\n" % thermostat )
        
if __name__=="__main__":

    import sys
    f = sys.stdout
    import Numeric as N
    xa = N.zeros((1,3),N.Float)
    va = xa + 1.0
    va2= va*va
    logger(f,2, xa, va, (1.2,3.4))
    f.write("Any Python object with s format  %s \n" % va2 )
    f.write("Any Python object with r format  %r \n" % va2 )
    f.write("Several Python objects need tuplification  %s %s \n" % (xa, va2) )
    
    
