Feature: I can play a tournament

	 Scenario: play a simple tournament
	 	   Given a tournament
		   When I enter "J"
		   When I enter "c"
		   When I enter "0"
		   When I enter "o"
		   When I enter "j"
		   # Round 1
		   When I enter "0"
		   When I enter "1"
		   When I enter "2"
		   When I enter "0"
		   # Round 2
		   When I enter "1"
		   When I enter "0"
		   When I enter "2"
		   When I enter "0"
		   # Round 3
		   When I enter "2"
		   When I enter "2"
		   When I enter "0"
		   When I enter "1"

		   When I enter "q"
		   When I enter "q"
		   Then player Kazparov score is 1.5
		   Then player Carlsen score is 0.5
		   Then player Fischer score is 0.5
		   Then player Capablanca score is 2.5
		   Then player Karpov score is 1.5
		   Then player Botvinnik score is 2.5
		   Then player Kramnik score is 2.0
		   Then player Lasker score is 1.0
		   