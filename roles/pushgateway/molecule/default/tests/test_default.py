from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        "/var/lib/pushgateway"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/pushgateway.service",
        "/usr/local/bin/pushgateway"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_permissions_didnt_change(host):
    dirs = [
        "/etc",
        "/root",
        "/usr",
        "/var"
    ]
    for file in dirs:
        f = host.file(file)
        assert f.exists
        assert f.is_directory
        assert f.user == "root"
        assert f.group == "root"


def test_user(host):
    assert host.group("pushgateway").exists
    assert "pushgateway" in host.user("pushgateway").groups
    assert host.user("pushgateway").shell == "/usr/sbin/nologin"
    assert host.user("pushgateway").home == "/"


def test_service(host):
    s = host.service("pushgateway")
#    assert s.is_enabled
    assert s.is_running


def test_protecthome_property(host):
    s = host.service("pushgateway")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9091"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
