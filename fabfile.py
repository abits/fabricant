#!/bin/env python2

from fabric.api import *
from fabric.utils import *
from fabric.colors import *
import telnetlib
import os
from time import sleep

# sudo mount 10.0.2.2:/home/chm/temp/wheezy-kvm tmp
# /home/chm/temp/wheezy-kvm  127.0.0.1(rw,no_root_squash,insecure)
# ansible wheezy64 --private-key vagrant.key -u vagrant --sudo -i ansible/host -a "date"

qemu_system_cmd = '/usr/bin/qemu-system-x86_64'
qemu_base_box = '/home/chm/VirtualMachines/wheezy64.qcow2.bz2'
qemu_img = '/home/chm/VirtualMachines/wheezy64.qcow2'
qemu_vm_name = 'wheezy64'
qemu_device_options = 'e1000,netdev=user.0'
qemu_monitor_host = '127.0.0.1'
qemu_monitor_port = '4444'
qemu_monitor_address = '%s:%s' % (qemu_monitor_host, qemu_monitor_port)
qemu_monitor_options = 'telnet:%s,server,nowait' % qemu_monitor_address
qemu_host_ssh_port = '5555'
qemu_guest_ssh_port = '22'
qemu_netdev_options = 'user,id=user.0,hostfwd=tcp::%s-:%s' % (qemu_host_ssh_port, qemu_guest_ssh_port)
qemu_generic_options = '-enable-kvm -serial null -parallel null -display none -vga none -daemonize'
qemu_cmd = '%s %s -name %s -device %s -netdev %s -monitor %s -boot d %s' % (qemu_system_cmd,
                                                                            qemu_generic_options,
                                                                            qemu_vm_name,
                                                                            qemu_device_options,
                                                                            qemu_netdev_options,
                                                                            qemu_monitor_options,
                                                                            qemu_img)
shared_folders = [('/home/chm/temp/wheezy-kvm', '/home/vagrant/tmp'), ('/home/chm/temp/wheezy-kvm/www', '/srv/www/sdk')]
qemu_fab_user = 'vagrant'
qemu_fab_group = 'vagrant'
qemu_fab_host = '%s@localhost:%s' % (qemu_fab_user, qemu_host_ssh_port)

env.key_filename = ["vagrant.key"]

@task
def vm(action='start'):
    if action == 'start':
        local(qemu_cmd)
        msg = 'Started virtual machine %s. Mapping guest port %s to host port %s. Telnet monitor on: %s.' % (qemu_vm_name,
                                                                                                             qemu_guest_ssh_port,
                                                                                                             qemu_host_ssh_port,
                                                                                                             qemu_monitor_address)
        puts(green(msg))

    elif action == 'stop':
        monitor = telnetlib.Telnet()
        monitor.open(qemu_monitor_host, qemu_monitor_port)
        monitor.write("system_powerdown\n")
        monitor.close()
        msg = 'Stopped virtual machine %s.' % qemu_vm_name
        puts(green(msg))
    elif action == 'up':
        if not os.path.exists(qemu_img):
            puts(green('Unpacking base box.'))
            decompress_cmd = 'bunzip2 -q %s' % qemu_base_box
            local(decompress_cmd)
        nfs(cmd='start')
        vm(action='start')
        sleep(10)
        nfs(cmd='mount')
        vm(action='provision')
    elif action == 'provision':
        with hide('running', 'stderr', 'stdout', 'warnings'):
            local('ansible -v wheezy64 -a "apt-get -y install python-apt" -u vagrant -s -i ansible/host --private-key vagrant.key')
        local('ansible-playbook ansible/default.yml --private-key vagrant.key -u vagrant --sudo -i ansible/host')


@task
@hosts(qemu_fab_host)
def nfs(cmd='start'):
    '''Manage nfs services (your mileage may vary).'''

    if cmd == 'start':
        local('sudo systemctl restart rpc-idmapd')
        local('sudo systemctl restart rpc-mountd')
    elif cmd == 'stop':
        local('sudo systemctl stop rpc-idmapd')
        local('sudo systemctl stop rpc-mountd')
    elif cmd == 'prepare':
        begin_marker = 'BEGIN_KVM: %s' % qemu_vm_name
        end_marker = 'END_KVM: %s' % qemu_vm_name
        declaration_form = '%s  127.0.0.1(rw,all_squash,insecure,no_subtree_check)'
        # TODO: modify /etc/exports
    elif cmd == 'mount':
        puts(green('Mounting NFS shared folders.'))
        with hide('running', 'stderr', 'stdout', 'warnings'):
            for folder in shared_folders:
                with settings(warn_only=True):
                    host, guest = folder
                    mkdir_cmd = 'sudo mkdir -p -m 0755 %s' % guest
                    run(mkdir_cmd)
                    mount_cmd = 'sudo mount 10.0.2.2:%s %s' % folder
                    run(mount_cmd)


@task
def ssh():
    ssh_cmd = 'ssh -A -i %s -p %s %s@localhost' % (env.key_filename[0], qemu_host_ssh_port, qemu_fab_user)
    local(ssh_cmd)
