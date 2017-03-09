Feature: dcos-metronome-python can create and list metronome jobs

  Scenario: Metadata can be fetched
    Given a working metronome instance
    Then we get the metronome pong

  Scenario: Trivial jobs can be created
    Given a working metronome instance
    When we create a trivial new job
    Then we should see the trivial job running via the metronome api

  Scenario: Complex jobs can be created
    Given a working metronome instance
    When we create a complex new job
    Then we should see the complex job running via the metronome api

  Scenario: A job can be create with a disk value at zero
    Given a working metronome instance
    When we create a new job with disk value at zero
    Then we should see the job running with disk value at zero via the metronome api

  Scenario: A job can be create without cmd field
    Given a working metronome instance
    When we create a new job without cmd field
    Then we should see the job running without cmd field via the metronome api

  Scenario: A job can be updated
    Given a working metronome instance
    When we create a trivial new job
    Then we should update a above job via the metronome api

  Scenario: A job can be deleted
    Given a working metronome instance
    When we create a trivial new job
    Then we should delete a job via the metronome api