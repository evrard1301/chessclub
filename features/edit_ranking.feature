Feature: I can edit the ranking of the players

	 Scenario: change ranking
	 	   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Garry Kazparov" ranking is 5
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Magnus Carlsen" ranking is 3
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Bobby Fischer" ranking is 1
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Jose Raul Capablanca" ranking is 7
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Anatoly Karpov" ranking is 2
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Mikhail Botvinnik" ranking is 6
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Vladimir Kramnik" ranking is 4
		   
		   Given eight players
		   When I enter sequence "c,m,5,3,1,7,2,6,4,8,q,q"
		   Then "Emanuel Lasker" ranking is 8
