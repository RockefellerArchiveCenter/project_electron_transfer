# Aurora QA Tests - Appraisal

These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Feature: Allow appraisal archivists to search and sort transfers  

	Scenario: appraisal archivist searches for transfer by creator
		Given one or more transfers exist in Appraisal Queue UI
		When user enters search into search field
		Then display search results with matching creator  

	Scenario: appraisal archivist searches for transfer by title
		Given one or more transfers exist in Appraisal Queue UI
		When user enters search into search field
		Then display search results with matching title  

	Scenario: appraisal archivist searches for transfer by date transferred
		Given one or more transfers exist in Appraisal Queue UI
		When user enters search into search field
		Then display search results with matching date transferred  

	Scenario: appraisal archivist searches for transfer by record type
		Given one or more transfers exist in Appraisal Queue UI
		When user enters search into search field
		Then display search results with matching record type  

	Scenario: appraisal archivist sorts by creator
		Given one or more transfers exist in Appraisal Queue UI
		When user clicks on creator column
		Then sort creator column by ascending or descending  

	Scenario: appraisal archivist sorts by title
		Given one or more transfers exist in Appraisal Queue UI
		When user clicks on title column
		Then sort title column by ascending or descending  

	Scenario: appraisal archivist sorts by transferred date
		Given one or more transfers exist in Appraisal Queue UI
		When user clicks on date transferred column
		Then sort date transferred column by ascending or descending  

	Scenario: appraisal archivist sorts by record type
		Given one or more transfers exist in Appraisal Queue UI
		When user clicks on record type column
		Then sort record type column by ascending or descending

## Feature: Allow appraisal archivists to add appraisal notes to transfers  

	Scenario: appraisal archivist adds note to transfer
		Given user is logged in
			And user has permissions to add appraisal notes
			And transfer exists in Appraisal Queue UI
		Then allow user to enter appraisal note
			And save note in Aurora

	Scenario: appraisal archivist edits transfer note
		Given user is logged in
			And user has permissions to edit appraisal notes
			And transfer exists in Appraisal Queue UI
			And transfer already has saved transfer note information
		Then allow user to view existing appraisal note
			And allow user to edit existing appraisal note
			And save updated note in Aurora

	Scenario: non-appraisal archivist tries to add note to transfer
		Given user is logged in
			And user does not have permissions to add or edit appraisal notes
			And one or more transfers exist in Appraisal Queue UI
		Then do not allow user to add new appraisal notes
			And do not allow user to edit existing appraisal notes

## Feature: Allow appraisal archivists to accept or reject transfers  

	Scenario: appraisal archivist accepts a transfer
		Given a user is logged in
			And the user has permissions to approve or reject transfers
		When the appraisal archivist deems transfer is within collecting scope
		Then transfer status is updated in Aurora
			And transfer automatically moves to the Accessioning Queue
			And transfer disappears from Appraisal Queue UI
			And user is returned to Appraisal Queue UI

	Scenario: appraisal archivist rejects a transfer
		Given a user is logged in
			And the user has permissions to approve or reject transfers
		When the appraisal archivist deems transfer is not within collecting scope
		Then transfer status is updated in Aurora
			And email containing appraisal note is delivered to donor
			And transfer is deleted
			And user is returned to Appraisal Queue UI
