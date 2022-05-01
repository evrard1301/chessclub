Feature: I can create a player

	 Scenario: create a simple male player
	 	   Given a new session
		   When I select j
		   When I set the last name to be Boben
		   When I set the first name to be Ludivic
		   When I set the date of birth to be 13/01/1995
		   When I set the gender to be M
		   When I set the ranking to be 7
		   Then a new player is created

	 Scenario: create a simple female player
	 	   Given a new session
		   When I select j
		   When I set the last name to be Sapin
		   When I set the first name to be Johanne
		   When I set the date of birth to be 12/08/98
		   When I set the gender to be F
		   When I set the ranking to be 2
		   Then a new player is created