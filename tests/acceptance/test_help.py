import pexpect


def test_help():
    sut = pexpect.spawn('python universal_deployer.py -h')
    sut.wait()
    sut.expect('usage')
    assert sut.exitstatus == 0
