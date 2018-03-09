# Project Electron QA Tests for Accessioning

These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Feature: Automatically group multiple transfers into single accession

	Scenario: bags related to each other via Bag-Count and Bag-Group-Identifier are grouped into the same accession
		Given multiple bags have the same Bag-Group-Identifier
			And all bags with the same Bag-Group-Identifier contain a Bag-Count
		When bags are accepted by an appraisal archivist
		Then group all transfers with the same Bag-Group-Identifier together
			And display as single accession in Accessioning Queue UI

	Scenario: transfers related to each other via source organization, record creator, and record type are grouped into the same accession
		Given multiple transfers match on source organization
			And record creator matches
			And record type matches
			And transfers have been approved by an appraisal archivist
		When Accessioning Queue UI is loaded
		Then transfers are grouped together
			And displayed as single accession in Accessioning Queue UI

	Scenario: transfers related to each other via record creator and record type are not grouped into the same accession
		Given multiple transfers do not match on source organization
			And record creator matches
			And record type matches
			And transfers have been approved by an appraisal archivist
		When Accessioning Queue UI is loaded
		Then transfers are not grouped into single accession
			And multiple accessions are displayed in the Accessioning Queue UI

	Scenario: transfers related to each other via source organization and record type are not grouped into the same accession
		Given multiple transfers match on source organization
			And record creator does not match
			And record type matches
			And transfers have been approved by an appraisal archivist
		When Accessioning Queue UI is loaded
		Then transfers are not grouped into single accession
			And multiple accessions are displayed in the Accessioning Queue UI

	Scenario: transfers related to each other via source organization and record creator are not grouped into the same accession
		Given multiple transfers match on source organization
			And record creator matches
			And record type does not match
			And transfers have been approved by an appraisal archivist
		When Accessioning Queue UI is loaded
		Then transfers are not grouped into single accession
			And multiple accessions are displayed in the Accessioning Queue UI

	Scenario: transfers not related to each other via source organization, record creator, and record type are not grouped into the same accession
		Given multiple transfers match on source organization
			And record creator matches
			And record type matches
			And transfers have not been approved by an appraisal archivist
		When Accessioning Queue UI is loaded
		Then transfers are not grouped into single accession
			And transfers are not displayed in the Accessioning Queue UI

## Feature: Allow accessioning archivists to search and sort accessions

	Scenario: accessioning archivist searches for accession by creator
		Given accession exists in Accessioning Queue UI
			And accession with a Source-Organization and one or more Record-Creators exists in Accessioning Queue UI
		When user enters search into search field
		Then display search transfer with creator(s) matching query string

	Scenario: accessioning archivist searches for accession by record type
		Given one or more accessions exist in Accessioning Queue UI
		When user enters search into search field
		Then display search results with matching record type

	Scenario: accessioning archivist sorts by creator
		Given one or more accessions exist in Accessioning Queue UI
		When user clicks on creator column
		Then sort creator column by ascending or descending

	Scenario: accessioning archivist sorts by title
		Given one or more accession exists in Accessioning Queue UI
		When user clicks on title column
		Then sort title column by ascending or descending

	Scenario: accessioning archivist sorts by record type
		Given one more more accession exists in Accessioning Queue UI
		When user clicks on record type column
		Then sort record type column by ascending or descending

## Feature: Allow accessioning archivists to review accession records

	Scenario: accessioning archivist reviews accession records
		Given user is logged in
		 	And user has permission to view Accessioning Queue UI
		When user selects "Accession" in Accessioning Queue UI
		Then show Accession Approval view
			And autopopulate accession record fields
			And allow user to view contents of each field
			And allow user to edit select accession record fields
			And allow user to save updated accession
			And send requests to microservices

## Feature: Create a DACS-compliant accession record in ArchivesSpace that includes donor-submitted metadata and as any description created by an appraisal archivist

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

## Feature: Validate target resource record field in Aurora Accession Record UI

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

## Feature: Validate agents in Aurora Accession Record UI

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

## Feature: Allow external application to update transfer status

	Scenario: Update transfer status in Aurora
		Given a transfer exists in Aurora
		When an external system sends a request to update the status of that transfer
		Then the transfer status is updated in Aurora
			And a response indicating success is sent to the external system
