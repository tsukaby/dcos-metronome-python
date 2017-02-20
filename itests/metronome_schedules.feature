Feature: dcos-metronome-python can CRUD for schedules

  Scenario: A schedule can be created
    Given a working metronome instance
    When we create a schedule
    Then we should see the schedule via the metronome api

  Scenario: A schedule can be updated
    Given a working metronome instance
    When we update a schedule
    Then we should see the updated schedule via the metronome api

  Scenario: A schedule can be deleted
    Given a working metronome instance
    When we delete a schedule
    Then we should not see the schedule via the metronome api

