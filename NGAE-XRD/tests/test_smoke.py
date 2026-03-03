from ngae_xrd import __version__


def test_version_present() -> None:
    assert isinstance(__version__, str)
    assert len(__version__) > 0
