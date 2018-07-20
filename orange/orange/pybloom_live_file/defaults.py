import os

BLOOM_FILE_NAME = 'bloom_file'
BLOOM_FILE_PATH = '%(path)s%(sep)s' % {'path': os.path.split(__file__)[0], 'sep': os.path.sep}

# bloom file save period
SAVE_PERIOD = 3
# bloom config
BLOOM_CAPACITY = 1000000
BLOOM_ERROR_RATE = 0.001
