# Aurora Post-Microservice QA Tests

In addition to tests specified in `Aurora Pre-Microservice QA Tests`, Aurora should pass all of the tests below once Project Electron microservices have been implemented. These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Accessioning

#### Feature: Create a DACS-compliant accession record in ArchivesSpace that includes donor-submitted metadata and as any description created by an appraisal archivist

	Scenario: a DACS-compliant accession record is created in ArchivesSpace when a resource record already exists
		Given a valid accession record in Aurora
			And a linked resource record in ArchivesSpace
		When user saves accession record
		Then Aurora sends requests to microservices to create accession record
			And Aurora sends requests to microservices to create archival objects

	Scenario: a DACS-compliant accession record is not created in ArchivesSpace
		Given an invalid accession record in Aurora
			And a linked resource record in ArchivesSpace
		When user saves accession record
		Then Aurora presents error message specifying which fields are required but empty
			And Aurora does not send requests to microservices to create accession record
			And Aurora does not send requests to create archival objects

#### Feature: Validate target resource record field in Aurora Accession Record UI

	Scenario: a user types name of existing resource record
		Given target resource record exists in ArchivesSpace
		When user starts typing the title or identifier of that resource record
		Then name of resource record appears as an option to select
			And user selects the name of the appropriate resource record

	Scenario: a user types name of resource record that does not exist
		Given target resource record does not exist in ArchivesSpace
		When user starts typing the title or identifier of that resource record
		Then name of resource record does not appear as an option to select
			And user is not able to save the accession record

#### Feature: Validate agents in Aurora Accession Record UI

	Scenario: Source-Organization names matching existing ArchivesSpace agent records are marked as verified
		Given a valid accession record in Aurora
			And a string value exists for the Source-Organization key in that accession record
			And that string can be matched to the name of an existing agent in ArchivesSpace
		When user selects "Accession" in Accession Queue UI
		Then display the Source-Organization as a verified name in the Accession Approval window

	Scenario: Record-Creators names matching existing ArchivesSpace agent records are marked as verified
		Given a valid accession record in Aurora
			And a string value exists for one or more Record-Creators keys in that accession record
			And that string can be matched to the name of an existing agent in ArchivesSpace
		When user selects "Accession" in Accession Queue UI
		Then display the Record-Creator as a verified name in the Accession Approval window

	Scenario: Source-Organization names which do not match existing ArchivesSpace agent records are marked as unverified
		Given a valid accession record in Aurora
			And a string value exists for the Source-Organization key in that accession record
			And that string cannot be matched to the name of an existing agent in ArchivesSpace
		When user selects "Accession" in Accession Queue UI
		Then display the Source-Organization as an unverified name in the Accession Approval window

	Scenario: Record-Creators which do not match existing ArchivesSpace agent records are marked as unverified
		Given a valid accession record in Aurora
			And a string value exists for one or more Record-Creators key in that accession record
			And that string cannot be matched to the name of an existing agent in ArchivesSpace
		When user selects "Accession" in Accession Queue UI
		Then display that Record-Creators as an unverified name in the Accession Approval window

## General

#### Feature: Allow external application to update transfer status

	Scenario: Update transfer status in Aurora
		Given a transfer exists in Aurora
		When an external system sends a request to update the status of that transfer
		Then the transfer status is updated in Aurora
			And a response indicating success is sent to the external system
