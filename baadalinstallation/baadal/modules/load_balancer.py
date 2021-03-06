# -*- coding: utf-8 -*-
###################################################################################
# Added to enable code completion in IDE's.
if 0:
    from gluon import *  # @UnusedWildImport
    from applications.baadal.models import * 	
###################################################################################

import sys, math, shutil, paramiko, traceback, libvirt, os
import xml.etree.ElementTree as etree
from libvirt import *  # @UnusedWildImport
from helper import *  # @UnusedWildImport

from host_helper import *  # @UnusedWildImport
from vm_utilization import *
from nat_mapper import create_mapping, remove_mapping
from vm_helper import *
   

#############################################################################


def get_migration_vector(HMAX,HMIN):
	vector=(HMAX-HMIN)/2
	return vector
	

def load_balance():
    try:
    	logger.debug("Inside load balancer() function")
	hosts=get_active_hosts()
    	
	flag=0
	while True:
		flag=0
		hostMIN=hosts[0]
    		hostMAX=hosts[0]
	
	    	migration_vector=0
    		HMAX=0
    		HMIN=9999
    			    	
    		for host in hosts:
    			host_cpu_usage=get_host_cpu_usage(host['ip'])
			if host_cpu_usage > HMAX:
				HMAX=host_cpu_usage
				hostMAX=host
		
			if host_cpu_usage < HMIN:
				HMIN=host_cpu_usage
				hostMIN=host
		
    		migration_vector=get_migration_vector(HMAX,HMIN)
    		vms=get_host_domains_ID(hostMAX['ip'])
		
    		conn = libvirt.openReadOnly('qemu+ssh://root@'+hostMAX['ip']+'/system')	
    		dom_id=''
		diff_cpu=999
    		for vm_id in vms
			dom = conn.lookupByID(vm_id)
			dom_info=dom.info()
			if dom_info[0] == '1':
				usage=get_actual_usage(dom,hostMAX['ip'])
				dom_cpu=float(usage['cpu'])		
				diff=abs(migration_vector - dom_cpu)
				if diff < migration_vector and diff < diff_cpu:
					diff_cpu=diff
					dom_id=vm_id	
					flag=1
				
   		migrate_domain(dom_id,hostMIN['id'],True)		

		if flag==0:
			break
       
    except:
        logger.debug("Task Status: FAILED Error: %s " % log_exception())
        return (current.TASK_QUEUE_STATUS_FAILED, log_exception())





#############################################################################

#take all migrate vm function from host_helper
def proactive_fault_tolerance():
	try:
		logger.debug("Inside proactive fault tolerance function")
	    	#hosts=get_all_host()
		hosts=get_active_hosts()
		max_temp_host=hosts[0]
		min_temp_host=hosts[0]
		critical_temp=105.0	
		high_temp=87.0	
		host_max_temp=0
		host_min_temp=999
		while True:
			for host in hosts:
				command='cputemp -C -a -s 3 | tail -1'
				command_output=execute_remote_cmd(host['ip'],'root',command,None,True)
				cpu_temp=float(command_output[0])
				
				if host_max_temp < cpu_temp:
					host_max_temp=cpu_temp
					max_temp_host=host

				if host_min_temp > cpu_temp:
					host_min_temp=cpu_temp
					min_temp_host=host			 

			
			

				 


