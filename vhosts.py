#!/usr/bin/env python
#coding: utf-8

import nginx
import apache
import sys
from config import *
import os

if __name__ == '__main__':
    if sys.argv[1] == 'php':
        logging.debug("Start add_php_vhost procedure")
        if len(sys.argv) == 4:
            logging.debug("Ok. 4 sys.argv")

            domain_name = sys.argv[2]
            logging.info("Domain: %s" % domain_name)

            document_root = sys.argv[3]
            logging.info("Document Root: %s" % document_root)
            docroot_exists = os.path.isdir(document_root)

            if docroot_exists:
                logging.debug("OK. Document Root is valid directory")
            else:
                logging.error("FAILED. Document Root does not exist.")
                sys.exit(1)

            logging.debug("Add proxy vhost on nginx")
            try:
                nginx.add_proxy_vhost(domain_name)
		nginx.enable_vhost(domain_name)
            except Exception, exc:
                logging.error("FAILED. %s" % exc)
                sys.exit(1)
            else:
                logging.debug("Succeded.")

            logging.debug("Add PHP vhost on Apache")
            try:
                apache.add_php_vhost(domain_name, document_root)
		apache.enable_vhost(domain_name)
            except Exception, exc:
                logging.error("FAILED. %s" % exc)
                sys.exit(1)
            else:
                logging.debug("Succeded.")
        else:
            logging.error("Wrong number of arguments.")
            print "Usage: %s php domain_name document_root_path" % sys.argv[0]
            sys.exit(1)
    elif sys.argv[1] == 'delete':
	if len(sys.argv) == 3:
	    domain_name = sys.argv[2]
	    nginx.disable_vhost(domain_name)
            nginx.delete_vhost(domain_name)
            apache.disable_vhost(domain_name)
            apache.delete_vhost(domain_name)
	else:
	    logging.error("Worng number of arguments.")
            print "Usage: %s delete domain_name" % sys.argv[0]
	    sys.exit(1)