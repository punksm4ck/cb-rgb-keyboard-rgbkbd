
def test_effect_start():
    from effects.engine.base import BaseEffect
    e = BaseEffect(None)
    e.start()
    assert e.running

def test_effect_stop():
    from effects.engine.base import BaseEffect
    e = BaseEffect(None)
    e.start()
    e.stop()
    assert not e.running
