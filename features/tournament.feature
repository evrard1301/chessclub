Feature: I can create a tournament

	 Scenario: create a simple tournament
	 	   Given eight players
		   When I enter "t"
		   When I add player "0"
		   When I add player "1"
		   When I add player "2"
		   When I add player "3"
		   When I add player "4"
		   When I add player "5"
		   When I add player "6"
		   When I add player "7"
		   When I add a round from 13/01/2020 to 14/01/2020
		   When I add a round from 15/01/2020 to 16/01/2020
		   When I add a round from 17/01/2020 to 18/01/2020
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "3/2/2"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament is successfully created
		   