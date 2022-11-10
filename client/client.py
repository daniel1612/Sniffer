import socket
from pseudoTCP import PseudoTCPClient


message = """
Chapter 1: The Other Minister
"The trouble is, the other side can do magic too, Prime Minister."
— Rufus Scrimgeour, to the Muggle Prime Minister.
Portrait of Ulick Gamp in the Prime Minister's office
The Muggle Prime Minister receives a notice that Cornelius Fudge is to meet him. 
He then recollects Fudge's earlier meetings with him: his first meeting with Fudge soon after he became the Prime Minister, 
Sirius Black's escape from Azkaban, the Quidditch World Cup, 
the Triwizard Tournament and the 1996 Azkaban mass breakout. 
When Fudge finally arrives, he reveals a number of incidents 
which had occurred in the Muggle world and for which the Prime 
Minister is forced to owe responsibility: the collapse of 
the Brockdale Bridge, a supposed hurricane in the West Country, 
the deaths of Amelia Bones and Emmeline Vance and the insanity of Junior Minister Herbert 
Chorley which have all been caused by Lord Voldemort, 
his followers the Death Eaters and their Giant allies. In short, 
the Second Wizarding War has begun. Fudge also reveals that he has been sacked and replaced by 
Rufus Scrimgeour as Minister for Magic. Scrimgeour too meets the Prime 
Minister and discusses security arrangements with him. 
He also reveals that Fudge will be a laison between them.
Chapter 2: Spinner's End
"Do you really think that the Dark Lord has not asked me each and every one of those questions?
And do you really think that,
had I not been able to give satisfactory answers, 
I would be sitting here talking to you?"
— Snape, to Bellatrix Lestrange.
Bellatrix and Narcissa Malfoy at Snape's House
Narcissa Malfoy and her sister Bellatrix Lestrange visit Severus Snape at Spinner's End, 
a poverty-stricken neighbourhood in a northern mill town. 
Narcissa wants Snape to help her protect her son Draco,
who has been made a Death Eater and has been assigned a mission by Lord Voldemort himself. 
Bellatrix advises against this, 
distrusting Snape for not taking part in the Battle of the Department of Mysteries at the Ministry of Magic, 
and for his many suspicious actions through the years which make her doubt whether Snape is actually on their side. 
Snape explains his behaviour: He was at Hogwarts when Voldemort fell to be a spy for him, he didn't seek him out for 
the same reason her brother in law and the other deserters didn't look for him, he stopped Voldemort from getting the 
Philosopher's Stone because he thought Quirrell wanted it for himself, he never tried to kill Harry Potter 
because Dumbledore would know about it, and he didn't take part in the Battle of the Department of Mysteries 
because Voldemort ordered him to stay at Hogwarts. Snape also tells Narcissa that he knows about Draco's mission. 
Bellatrix tells her sister she should be proud but Narcissa believes that Voldemort is sending him on a 
suicide mission as punishment for her husband's failure. Snape offers to help Draco. Narcissa asks him to make an 
Unbreakable Vow and he agrees. With Bellatrix as their Bonder, Narcissa asks Snape to agree to the following terms:
That he watch over Draco while he attempts to carry out his mission as a Death Eater.
That he protect him and make sure he comes to no harm.
That he do the job for Draco if he proves unable to do it himself.
Snape agrees to all three terms and the vow is made.
"""
serverAddressPort = ("192.168.0.196", 12321)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

tcpInstance = PseudoTCPClient(UDPClientSocket,serverAddressPort)
tcpInstance.sendMsg(message)


