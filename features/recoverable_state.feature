Feature: the state of the program is not cleaned when
	 an action is canceled

	 Scenario: I can interrupt and continue a played tournament
	 	   Given a tournament
		   When I enter sequence "J,c,0,o,j"
		   # Round 1
		   When I enter sequence "0,1,2"
		   When I enter "\quitter"
		   When I enter sequence "J,c,0,o,j"
		   # Round 1 end
		   When I enter sequence "1"
		   # Round 2
		   When I enter sequence "2,2,1,0"
		   # Round 3
		   When I enter sequence "2,2,1,0"
		   When I enter sequence "q,q"
		   Then player Kazparov score is 2.0
		   Then player Carlsen score is 1
		   Then player Fischer score is 1.5
		   Then player Capablanca score is 2
		   Then player Karpov score is 0
		   Then player Botvinnik score is 2.0
		   Then player Kramnik score is 1.5
		   Then player Lasker score is 2.0
		   
	Scenario: I can quit and continue a created tournament
		  Given eight players
		  When I enter sequence "t"
		  # Give informations
		  When I enter sequence "i,Hello,World,12/08/1995"
		  When I enter sequence "blitz,description here"
		  When I enter sequence "q,t"
		  # Add players
		  When I enter sequence "j,0,j,1,j,2,j,3,j,4"	  
		  When I enter sequence "j,5,j,6,j,7"		  
		  # Add a round
  		  When I enter sequence "r,13/08/1998,14/08/1998"
		  When I enter sequence "q,t"
		  # create it
		  When I enter sequence "t,q,q"
		  Then 1 tournaments has been created

