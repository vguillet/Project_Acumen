from Group12.dbinterface.DBGUIAPI import DBManager



x = DBManager()

######################### Geogreaphy Subject ############################
x.add_new_subject("Geography")

x.add_new_topic("CapitalsOfTheEU","Geography")
x.add_new_question("CapitalsOfTheEU","What is the capital of Germany?","Berlin","Geography")
x.add_new_question("CapitalsOfTheEU","What is the capital of Lithuania?","Vilnius","Geography")
x.add_new_question("CapitalsOfTheEU","What is the capital of Latvia?","Riga","Geography")
x.add_new_question("CapitalsOfTheEU","What is the capital of Albania?","Tirana","Geography")
x.add_new_question("CapitalsOfTheEU","What is the capital of Ireland?","Dublin","Geography")

x.add_new_topic("CapitalsOfTheMiddleEast","Geography")
x.add_new_question("CapitalsOfTheMiddleEast","What is the capital of the United Arab Emirates?","Abu Dhabi","Geography")
x.add_new_question("CapitalsOfTheMiddleEast","What is the capital of the Oman?","Muscat","Geography")
x.add_new_question("CapitalsOfTheMiddleEast","What is the capital of the Qatar?","Doha","Geography")

x.add_new_topic("CapitalsOfTheAmericas","Geography")
x.add_new_question("CapitalsOfTheAmericas","What is the capital of Argentina?","Buenos Aires","Geography")
x.add_new_question("CapitalsOfTheAmericas","What is the capital of Brazil?","Brasilia","Geography")
x.add_new_question("CapitalsOfTheAmericas","What is the capital of Venezuela?","Caracas","Geography")
x.add_new_question("CapitalsOfTheAmericas","What is the capital of Lima?","Peru","Geography")
x.add_new_question("CapitalsOfTheAmericas","What is the capital of Bolivia?","La Paz","Geography")


################################ History Subject ####################################
x.add_new_subject("History")

x.add_new_topic("WorldWar2","History")
x.add_new_question("WorldWar2","During which year did the Battle of Britain begin in?","1940","History")
x.add_new_question("WorldWar2","During which year did the Axis offensive code named Operation Barbarossa begin in??","1941","History")
x.add_new_question("WorldWar2","During which year did the Germans launch the battle of Kursk?","1943","History")
x.add_new_question("WorldWar2","During which year did the attack on Pearl Harbor occur?","1941","History")
x.add_new_question("WorldWar2","During which year did the Battle of Midway occur?","1942","History")

x.add_new_topic("FrenchRevolution","History")
x.add_new_question("FrenchRevolution","During which month and  year did the Tennis Court Oath occur in?","June 1789","History")
x.add_new_question("FrenchRevolution","During which month and year did the Storming of the Bastille occur in?","July 1789","History")
x.add_new_question("FrenchRevolution","During which month and year was the Declartion of the Rights of Man and the Citizen written in?","August 1789","History")

