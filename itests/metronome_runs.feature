Feature: dcos-metronome-python can CRUD for runs

  Scenario: A run can be created
    Given a working metronome instance
    When we create a run
    Then we should see the run via the metronome api

  Scenario: A run can be stopped
    Given a working metronome instance
    When we stop a run
    Then we should see the stopped run via the metronome api
