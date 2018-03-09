# Aurora QA Tests - Transfer

These tests are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin), a structured language that can be used for both documentation and automated testing of software.

## Feature: validate bag size and filename

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

## Feature: check bag for viruses

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

## Feature: validate bag structure

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

## Feature: validate bag fixity

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

## Feature: validate bag metadata

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
