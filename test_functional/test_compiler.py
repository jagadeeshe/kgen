'''
Created on Jun 15, 2011

@author: jagadeesh
'''
import os
import unittest
import glob
from UserDict import UserDict
from StringIO import StringIO
from kgen import compiler


def get_file_content(fname):
    f = file(fname)
    content = f.read()
    f.close()
    return content

class CompilerTest(unittest.TestCase):
    
    def test_functional(self):
        options = UserDict()
        options.encoding = 'utf-8'
        datafiles = self.get_data_files()
        for infile, outfile, errfile in datafiles:
            print "testing... %s" % os.path.basename(infile)
            input = get_file_content(infile)
            output_stream = StringIO()
            error_stream = StringIO()
            compiler.compile(input, output_stream, error_stream, options)
            output = output_stream.getvalue()
            error = error_stream.getvalue()
            if error:
                self.assertEqual(error, get_file_content(errfile).decode(options.encoding))
            else:
                self.assertEqual(output.encode(options.encoding), get_file_content(outfile))
    
    def get_data_dir(self):
        curpath = os.path.abspath(__file__)
        curdir = os.path.dirname(curpath)
        return os.path.join(curdir, 'data')
    
    def get_data_files(self):
        path = self.get_data_dir() + "/*.input.txt"
        files = []
        for infile in glob.glob(path):
            outfile = infile.replace('.input.txt', '.output.txt')
            errfile = infile.replace('.input.txt', '.error.txt')
            files.append((infile, outfile, errfile))
        return files
    


if __name__ == "__main__":
    unittest.main()
