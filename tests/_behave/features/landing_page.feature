Feature: Landing Page

    Scenario: Get an overview
        Given I visit the home page
        Then I see the call to action "I want to help!" on the page
        And I see the call to action "Organize volunteers!" on the page
        And I see the section "What is it all about?"
        And I see the section "You can help at these locations:"
        And I see a button labeled "Login"
        And I see a button labeled "Start helping"
        And I see some statistics about the Volunteer Planner
        And I see a list of areas with their respective facilities
        And I see a navigation bar in the footer
