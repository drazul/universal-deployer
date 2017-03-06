import pexpect


def test_help():
    sut = pexpect.spawn('python udeploy/universal_deployer.py -h')
    sut.wait()
    sut.expect('usage')
    assert sut.exitstatus == 0
