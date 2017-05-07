import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize("name, version", [
    ('python', '2.7'),
])
def test_packages(Package, name, version):
    pkg = Package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize('path, user', [
    ('/etc/monasca/agent/agent.yaml', 'root'),
    ('/opt/monasca-agent/bin/monasca-forwarder', 'root'),
])
def test_monasca_agent_installed(File, path, user):
    f = File(path)

    assert f.exists
    assert f.user == user


@pytest.mark.parametrize('service_name', [
    ('monasca-collector'),
    ('monasca-forwarder'),
    ('monasca-statsd'),
])
def test_monasca_agent_service_enabled(Service, service_name):
    s = Service(service_name)

    assert s.is_enabled
