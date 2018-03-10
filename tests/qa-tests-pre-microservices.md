# Aurora Pre-Microservice QA Tests

Aurora should pass all of the tests below before any Project Electron microservices are implemented. These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Transfer

#### Feature: validate bag size and filename

	Scenario: bag size and filename validate successfully
		Given a bag does not contain special characters in the filename
			And the size is less than maximum size
		When size validation function runs
		Then success information is logged in Aurora
			And success notifications are delivered to client

	Scenario: bag is too big
		Given a bag size exceeds maximum size
		When size validation function runs
		Then the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: bag has invalid filename
		Given a bag has a special characters in a filename
		When filename validation function runs
		Then the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

#### Feature: check bag for viruses

	Scenario: no virus is found
		Given a bag does not contain a virus
		When virus check function runs
		Then negative results are returned for all files within a bag
			And success information is logged in Aurora

	Scenario: virus is found in bag
		Given a bag contains a virus
		When virus check function runs
		Then a positive result is returned for a file within a bag
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client
			And Marist sysadmins are notified

	Scenario: virus definitions are out of date
		Given virus definitions are outdated
		When virus check function runs
		Then virus definitions are updated
			And the virus check function runs

#### Feature: validate bag structure

	Scenario: bag is correctly structured
		Given bag contains bag declaration (bagit.txt) in top level of base directory
			And bag contains payload directory (/data)  in top level of base directory
			And bag contains payload manifest (manifest-<alg>.txt)  in top level of base directory
			And bag contains bag manifest (bag-info.txt)  in top level of base directory
		When bag validation function runs
		Then bagit validation succeeds
			And success information is logged in Aurora

	Scenario: bag is missing bag declaration (bagit.txt)
		Given the bag does not contain the bag declaration with the filename bagit.txt  in top level of base directory
		When bag validation function runs
		Then bagit validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: bag is missing payload manifest (manifest-<alg>.txt)
		Given the bag does not contain the payload manifest with the filename manifest-<alg>.txt  in top level of base directory
		When bag validation function runs
		Then bagit validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: bag is missing bag manifest (bag-info.txt)
		Given the bag does not contain the bag manifest with the filename bag-info.txt  in top level of base directory
		When bag validation function runs
		Then bagit validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: bag is missing payload directory (/data)
		Given the bag does not contain the payload directory with the name "data"  in top level of base directory
		When bag validation function runs
		Then bagit validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: payload directory (/data) is empty
		Given bag contains bag declaration (bagit.txt) in top level of base directory
			And bag contains payload directory (/data) in top level of base directory
			And bag contains payload manifest (manifest-<alg>.txt) in top level of base directory
			And bag contains bag manifest (bag-info.txt) in top level of base directory
		When bag validation function runs
		Then bagit validation succeeds
			And success information is logged in Aurora

#### Feature: validate bag fixity

	Scenario: all bitstreams are unchanged
		Given pre and post transfer checksums are identical
		When bag validation function runs
			And checksums are calculated
		Then bagit validation succeeds
			And success information is logged in Aurora

	Scenario: one or more file has changed
		Given one or more pre-transfer checksum does not match a post-transfer checksum
		When bag validation script is run
			And checksums are calculated
		Then bagit validation failes
			And error information is logged in Aurora
			And error notifications are delivered to client
			And bag is deleted

### Feature: validate bag metadata

	Scenario: all metadata validation checks pass
		Given bag which validates against bagit specification
			And bag includes valid metadata.json file
			And bag-info.txt contains required information
			And values in bag-info.txt conform to local vocabularies
			And values in bag-info.txt conform to local datatype rules
		When metadata validation function runs
		Then metadata validation passes
			And success information is logged in Aurora

	Scenario: metadata.json is invalid
		Given bag which validates against bagit specification
			And a file named metadata.json exists in payload directory (/data)
			And metadata.json is not valid JSON or JSON-LD
		When metadata validation function runs
		Then metadata validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: bag-info.txt is missing required fields
		Given bag which validates against bagit specification
			And bag-info.txt is missing required fields
		When metadata validation function runs
		Then metadata validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: non-repeatable fields repeat in bag-info.txt
		Given bag which validates against bagit specification
		 	And bag-info.txt has non-repeatable fields repeating
		When metadata validation function runs
		Then metadata validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: language datatype does not meet specifications
		Given bag which validates against bagit specification
			And bag-info.txt contains a value for Language which does not adhere to RAC datatype specification
		When metadata validation function runs
		Then metadata validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: date datatype does not meet specifications
		Given bag which validates against bagit specification
			And bag-info.txt contains a value for Date-Start, Date-End or Bagging-Date which does not adhere to RAC datatype specification
		When metadata validation function runs
		Then metadata validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

	Scenario: locally controlled vocabularies in bag-info.txt data types don’t adhere to spec
		Given bag which validates against bagit specification
			And donor has used an unauthorized term in Source-Organization or Record-Type
		When metadata validation function runs
		Then metadata validation fails
			And the bag is deleted
			And error information is logged in Aurora
			And error notifications are delivered to client

## Rights

#### Feature: automatically apply rights statements to transfers

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

#### Feature: Allow appraisal archivists to manage structured rights

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

## Appraisal

#### Feature: Allow appraisal archivists to search and sort transfers  

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

#### Feature: Allow appraisal archivists to add appraisal notes to transfers  

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

#### Feature: Allow appraisal archivists to accept or reject transfers  

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

## Accessioning

#### Feature: Automatically group multiple transfers into single accession

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

#### Feature: Allow accessioning archivists to search and sort accessions

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

#### Feature: Allow accessioning archivists to review accession records

	Scenario: accessioning archivist reviews accession records
		Given user is logged in
		 	And user has permission to view Accessioning Queue UI
		When user selects "Accession" in Accessioning Queue UI
		Then show Accession Approval view
			And autopopulate accession record fields
			And allow user to view contents of each field
			And allow user to edit select accession record fields
			And allow user to save updated accession

## User and Organization Administration

#### Feature: create user and organization accounts

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

#### Feature: update user and organization accounts

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

#### Feature: user permissions

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
