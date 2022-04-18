import logging
import sys

#Setting up logger (ERROR, WARNING, CRITICAL, DEBUG, INFO) so it writes to file std.log and to console
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    handlers=[
                        logging.FileHandler('std.log'),
                        logging.StreamHandler(sys.stdout)])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[
                        logging.FileHandler('std.log'),
                        logging.StreamHandler(sys.stdout)])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR,
                    handlers=[
                        logging.FileHandler('std.log'),
                        logging.StreamHandler(sys.stderr)])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING,
                    handlers=[
                        logging.FileHandler('std.log'),
                        logging.StreamHandler(sys.stdout)])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.CRITICAL,
                    handlers=[
                        logging.FileHandler('std.log'),
                        logging.StreamHandler(sys.stderr)])
