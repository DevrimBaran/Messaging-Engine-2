import logging
import sys


def pime2_logger():
    """
    Setting up logger (ERROR, WARNING, CRITICAL, DEBUG, INFO) so it writes to file std.log and to console
    """
    path = "../log/std.log"
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG,
                        handlers=[
                            logging.FileHandler(path),
                            logging.StreamHandler(sys.stdout)])

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(path),
                            logging.StreamHandler(sys.stdout)])

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.ERROR,
                        handlers=[
                            logging.FileHandler(path),
                            logging.StreamHandler(sys.stderr)])

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.WARNING,
                        handlers=[
                            logging.FileHandler(path),
                            logging.StreamHandler(sys.stdout)])

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.CRITICAL,
                        handlers=[
                            logging.FileHandler(path),
                            logging.StreamHandler(sys.stderr)])
    return logging
