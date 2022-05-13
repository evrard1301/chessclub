Feature: the state of the program is not cleaned when
	 an action is canceled

	 Scenario: stop a playing tournament
	 	   Given a tournament
		   When I enter sequence "J,c,0,o,j"
		   # Round 0
		   When I enter sequence "0,1,2"
		   When I enter "\quitter"
		   When I enter sequence "J,c,0,o,j"
		   # Round 0 end + Round 2
		   When I enter sequence "1,2,2,1,0"
		   # Round 3
		   When I enter sequence "2,2,1,0"
		   When I enter sequence "q,q"
		   Then player Kazparov score is 2.0
		   Then player Carlsen score is 1.5
		   Then player Fischer score is 1.0
		   Then player Capablanca score is 2
		   Then player Karpov score is 0
		   Then player Botvinnik score is 2.0
		   Then player Kramnik score is 1.5
		   Then player Lasker score is 2.0