# Aurora QA Tests - Rights Management

These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Feature: automatically apply rights statements to transfers

	Scenario: default rights statements are applied to the transfer  
		Given an organization exists in Aurora  
			And that organization has a valid BagIt Profile containing one or more record types
			And default PREMIS-compliant rights exist for that organization and each record type
		When rights assignment function runs
		Then assign one or more PREMIS-compliant rights statement based on organization and record type
			And display rights assignment on transfer detail page
			And route transfer to Appraisal Queue

	Scenario: Default PREMIS rights statements are missing
		Given an organization exists in Aurora
			And that organization has a valid BagIt Profile containing one or more record types
			And default PREMIS-compliant rights do not exist for that organization and each record type
		When rights assignment function runs
		Then do not assign PREMIS rights statements
			And do not display rights assignment on transfer detail page
			And route transfer to Appraisal Queue

	Scenario: BagIt Profile is missing
		Given an organization exists in Aurora
			And that organization does not have a valid BagIt Profile containing one or more record types
			And default PREMIS-compliant rights exist for that organization
		When rights assignment function runs
		Then do not assign PREMIS rights statements
			And do not display rights assignment on transfer detail page
			And route transfer to Appraisal Queue

## Feature: Allow appraisal archivists to manage structured rights

	Scenario: user creates rights statement
		Given user has permissions to create rights statements
			And a given organization account exists
		Then user can create rights statements
			And the new rights statement is associated with an organization
			And the new rights statement is associated with one or more record types
			And the new rights statement is saved in Aurora

	Scenario: user edits rights statement
		Given user has permissions to edit rights statements
			And a given organization account exists
		Then user can edit rights statements
			And the edited rights statement is associated with an organization
			And the edited rights statement is associated with one or more record types
			And the edited rights statement is saved in Aurora
