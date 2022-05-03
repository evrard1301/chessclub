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
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament is successfully created

	 Scenario: create a tournament with only 7 players
	 	   Given eight players
		   When I enter "t"
		   When I add player "0"
		   When I add player "1"
		   When I add player "2"
		   When I add player "3"
		   When I add player "4"
		   When I add player "5"
		   When I add player "6"
		   When I add a round from 13/01/2020 to 14/01/2020
		   When I add a round from 15/01/2020 to 16/01/2020
		   When I add a round from 17/01/2020 to 18/01/2020
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament creation failed

	Scenario: create a tournament with two identical players
	 	   Given eight players
		   When I enter "t"
		   When I add player "0"
		   When I add player "1"
		   When I add player "2"
		   When I add player "3"
		   When I add player "3"
		   When I add player "5"
		   When I add player "6"
		   When I add player "7"
		   When I add a round from 13/01/2020 to 14/01/2020
		   When I add a round from 15/01/2020 to 16/01/2020
		   When I add a round from 17/01/2020 to 18/01/2020
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament creation failed

	 Scenario: create a tournament without round
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
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament creation failed

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
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
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
		   When I enter name "MyTournament2"
		   When I enter place "Elsewhere"
		   When I enter date "04/02/20"
		   When I enter category "blitz"
		   When I enter description "desc2"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then 2 tournaments has been created
		   
	Scenario: create a round where end date is earlier than start date 
		  Given eight players
		  When I enter "t"
		  When I add a round from 13/01/2020 to 12/01/2020
		  Then the tournament creation failed

	 Scenario: create a tournament where the category is invalide
	 	   Given eight players
		   When I enter "t"
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "03/02/20"
		   When I enter category "random name"
		   Then the tournament creation failed

	 Scenario: a round starts during another round
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
		   When I add a round from 13/01/2020 to 17/01/2020
		   When I add a round from 15/01/2020 to 19/01/2020
		   When I add a round from 17/01/2020 to 18/01/2020
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament creation failed

	 Scenario: a round ends during another round
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
		   When I add a round from 13/01/2020 to 16/01/2020
		   When I add a round from 15/01/2020 to 18/01/2020
		   When I add a round from 17/01/2020 to 18/01/2020
		   When I enter "i"
		   When I enter name "MyTournament"
		   When I enter place "Here"
		   When I enter date "03/02/20"
		   When I enter category "bullet"
		   When I enter description "desc"
		   When I enter "t"
		   When I enter "q"
		   When I enter "q"
		   Then the tournament creation failed

