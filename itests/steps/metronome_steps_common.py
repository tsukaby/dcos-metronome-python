from behave import given, then
from itest_utils import get_metronome_connection_string

import metronome


@given(u'a working metronome instance')
def step_impl(context):
    """Adds a working metronome client as context.client for the purposes of
    interacting with it in the test."""
    if not hasattr(context, 'client'):
        metronome_connection_string = "http://%s" % \
                                     get_metronome_connection_string()
        context.client = metronome.MetronomeClient(metronome_connection_string)


@then(u'we get the metronome pong')
def step_impl(context):
    assert context.client.ping() == 'pong'
