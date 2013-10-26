# -*- coding: utf-8 -*-

import argparse
import os
import yaml


class Settings(object):
    action = None
    options_file = 'fabricant.yml'
    options = None
    fabricant_dir = '.fabricant'
    base_boxes_dir = os.path.join(fabricant_dir, 'base')


    qemu_system_cmd = '/usr/bin/qemu-system-x86_64'
    qemu_base_box = '/home/chm/VirtualMachines/wheezy64.qbox'
    qemu_img = '/home/chm/VirtualMachines/wheezy64.qcow2'
    qemu_vm_name = 'wheezy64'
    qemu_device_options = 'e1000,netdev=user.0'
    qemu_monitor_host = '127.0.0.1'
    qemu_monitor_port = '4444'
    qemu_monitor_address = '%s:%s' % (qemu_monitor_host, qemu_monitor_port)
    qemu_monitor_options = 'telnet:%s,server,nowait' % qemu_monitor_address
    qemu_port_forwards = {
        '5555': '22',
        '8080': '80',
        '9933': '993'
    }
    qemu_fw_parameter = ''
    for host, guest in qemu_port_forwards.iteritems():
        mapping = ',hostfwd=tcp::%s-:%s' % (host, guest)
        qemu_fw_parameter += mapping
        if guest == '22':
            qemu_host_ssh_port = host
    qemu_netdev_options = 'user,id=user.0%s' % qemu_fw_parameter
    qemu_generic_options = '-enable-kvm -serial null -parallel null -display none -vga none -daemonize'
    qemu_cmd = '%s %s -name %s -device %s -netdev %s -monitor %s -boot d %s' % (qemu_system_cmd,
                                                                                qemu_generic_options,
                                                                                qemu_vm_name,
                                                                                qemu_device_options,
                                                                                qemu_netdev_options,
                                                                                qemu_monitor_options,
                                                                                qemu_img)
    shared_folders = [('/home/chm/temp/fabricant', '/home/vagrant/fabricant'), ('/home/chm/temp/fabricant/www', '/srv/www/sdk')]
    qemu_fab_user = 'vagrant'
    qemu_fab_group = 'vagrant'
    qemu_fab_host = '%s@localhost:%s' % (qemu_fab_user, qemu_host_ssh_port)
    
    key_filename = ["vagrant.key"]

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("action", help="action to run")
        parser.add_argument('--file', '-f', action="store", dest=self.options_file, help='Define default options file.')
        args = parser.parse_args()
        self.action = args.action
        self._load_options_from(self.options_file)


    def _load_options_from(self, options_file):
        options_file_path = os.path.join(os.getcwd(), options_file)
        if os.path.exists(options_file_path):
            stream = file(options_file_path, 'r')
            self.options = yaml.safe_load(stream)

