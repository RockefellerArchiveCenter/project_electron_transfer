# Aurora QA Tests - User and Organization Administration

These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Feature: create user and organization accounts

	Scenario: Create a new user
		Given a user is logged in
			And user has permissions to add new user accounts
		When a valid email address is provided for a new user account
		Then new user account is assigned an LDAP user ID
			And user account is added to LDAP
			And user ID is added to Aurora
			And success notification is logged in Aurora
			And success notification is displayed
			And email notification is sent to new user with link to reset password

	Scenario: Create a new organization
		Given a user is logged in
			And  user has permissions to add new organization accounts
		When organization information is entered
		Then new organization name is assigned to an LDAP group ID
			And directories are created for the organization
			And organization information is added to LDAP
			And organization ID is added to Aurora
			And organization status is marked as active
			And success notification is logged in Aurora
			And success notification is displayed

## Feature: update user and organization accounts

	Scenario: add a user to an organization
		Given a user is logged in
			And user has permissions to edit user and organization accounts
			And a specified user account exists
			And a specified organization account exists
			And a specified organization account status is active
		When user assigns adds user account to organization account
		Then organization assignment is applied in LDAP
			And success notification is logged in Aurora
			And success notification is displayed

	Scenario: change a user password
		Given a user is logged in with valid email_1 and password_1
		When a user changes password_1 to password_2
		Then user can log in with the email_1 and password_2
			And user can no longer log in with email_1 and password_1
			And password change is applied in LDAP
			And success notification is logged in Aurora
			And success notification is displayed

	Scenario: reset a user password
		Given a user is not logged in
			And user enters a valid email address
		When a user selects to reset password
		Then an email notification is sent to user with a link to reset password
		When user follows email link to reset password
			And user enters a new password
		Then success notification is displayed
			And user is logged in to account
			And password change is applied in LDAP
			And success notification is logged in Aurora
			And success notification is displayed

	Scenario: change a user status to inactive
		Given a user is logged in
			And user has permissions to edit user accounts
			And a given user account exists
			And the user account status is active
		When user marks a user account as inactive
		Then user account status is designated as inactive in Aurora
			And success notification is logged in Aurora
			And success notification is displayed

	Scenario: change an organization status to inactive
		Given user is logged in
			And user has permissions to edit organization accounts
			And a given organization account exists
			And the organization account status is active
		When user marks organization account inactive
		Then organization account status is designated as inactive in Aurora
			And users that have been added to organization are designated inactive in Aurora
			And success notification is logged in Aurora
			And success notification is displayed

	Scenario: Edit organization acquisition type
		Given user is logged in
			And user has permissions to edit organization accounts
			And a given organization account exists
		Then user updates organization acquisition type
			And updated acquisition type is saved in Aurora

## Feature: user permissions

	Scenario: donor user permissions
		Given a user is active
			And user is not part of any groups
		When user successfully logs in
		Then user is redirected to Aurora dashboard
			And data on dashboard is scoped to user's organization
			And user can view a list of transfers they have submitted
			And user can view a list of transfers submitted by all users from their organization
			And user can view detail pages of transfers they have submitted
			And user can view detail pages of transfers submitted by all users from their organization
			And user can view rights statements for their organization
			And user can view BagIt profile for their organization
			And user can view their organization's profile page
			And user can view their own profile page
			And user can change their own password

	Scenario: appraisal archivist user permissions
		Given a user is active
			And user is assigned to appraisal archivist group
		When user successfully logs in
		Then user is redirected to Aurora dashboard
			And data on dashboard is scoped to all transfers
			And user can view a list of all transfers
			And user can view detail pages of all transfers
			And user can view rights statements for all organizations
			And user can view BagIt profiles for all organizations
			And user can view all organizations' profile pages
			And user can view their own profile page
			And user can change their own password
			And user can view appraisal queue
			And user can view accessioning queue
			And user can accept or reject transfers
			And user can add appraisal notes to transfers

	Scenario: accessioning archivist user permissions
		Given a user is active
			And user is assigned to accessioning archivist group
		When user successfully logs in
		Then user is redirected to Aurora dashboard
			And data on dashboard is scoped to all transfers
			And user can view a list of all transfers
			And user can view detail pages of all transfers
			And user can view rights statements for all organizations
			And user can view BagIt profiles for all organizations
			And user can view all organizations' profile pages
			And user can view their own profile page
			And user can change their own password
			And user can view appraisal queue
			And user can view accessioning queue
			And user can create accession records

	Scenario: managing archivist user permissions
		Given a user is active
			And user is assigned to accessioning archivist group
		When user successfully logs in
		Then user is redirected to Aurora dashboard
			And data on dashboard is scoped to all transfers
			And user can view a list of all transfers
			And user can view detail pages of all transfers
			And user can view rights statements for all organizations
			And user can view BagIt profiles for all organizations
			And user can view all organizations' profile pages
			And user can view their own profile page
			And user can change their own password
			And user can view appraisal queue
			And user can view accessioning queue
			And user can accept or reject transfers
			And user can add appraisal notes to transfers
			And user can create accession records
			And user can add new users
			And user can edit existing users
			And user can add new organizations
			And user can edit existing organizations
			And user can add new rights statements
			And user can edit existing rights statements
			And user can add new BagIt Profiles
			And user can edit existing BagIt Profiles

	Scenario: system administrator user permissions
		Given a user is active
			And user is assigned to accessioning archivist group
		When user successfully logs in
		Then user is redirected to Aurora dashboard
			And data on dashboard is scoped to all transfers
			And user can view a list of all transfers
			And user can view detail pages of all transfers
			And user can view rights statements for all organizations
			And user can view BagIt profiles for all organizations
			And user can view all organizations' profile pages
			And user can view their own profile page
			And user can change their own password
			And user can view appraisal queue
			And user can view accessioning queue
			And user can accept or reject transfers
			And user can add appraisal notes to transfers
			And user can create accession records
			And user can add new users
			And user can edit existing users
			And user can add new organizations
			And user can edit existing organizations
			And user can add new rights statements
			And user can edit existing rights statements
			And user can add new BagIt Profiles
			And user can edit existing BagIt Profiles
			And user can change system settings

	Scenario: a user who has not been added to an organization attempts to log in
		Given a user status is active
			And user has not been added to an organization
		When user enters a valid email address and password
		Then Aurora rejects the log in attempt
			And error notification is displayed

	Scenario: an inactive user attempts to log in
		Given a user status is inactive
		When user enters a valid email address and password
		Then Aurora rejects the log in attempt
		 	And error notification is displayed

	Scenario: a user attempts to log in with invalid email address
		Given a user status is active
			And user has been added to an organization
		When user enters an invalid email address
		Then Aurora rejects the log in attempt
			And error notification is displayed

	Scenario: a user attempts to log in with invalid password
		Given a user status in active
			And user has been added to an organization
		When user enters an invalid password
		Then Aurora rejects the log in attempt
			And error notification is displayed
