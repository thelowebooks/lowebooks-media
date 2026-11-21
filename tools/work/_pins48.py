import sys; sys.argv=['x']
from make_pins import *
P={
'mon_parents_list5': qlist_pin('parents','Thanksgiving conversation starters.',[
 "Can you tell me about an achievement you're most proud of?","Can you tell me about a risk you took that paid off?",
 "What's something you wish you had known when you were younger?","How have you seen the world change most significantly in your lifetime?",
 "What would you say has been the key to a happy and fulfilling life?"],'5 of 300 questions in','Ask one at the table'),
'mon_random_nutella': hook_pin('random','Thanksgiving trivia. No googling.','Ask the table','Which nut is used to make Nutella?','One of 300 questions in'),
'tue_memory_fred': hook_pin('memory','Ask Grandpa this on Thursday.','Then watch him light up','Who hosted the classic children\'s show "Mister Rogers\' Neighborhood"?','One of 500 questions in'),
'tue_couples_list5': qlist_pin('couples','Funny date night questions.',[
 "What's an unusual hobby you've always wanted to try together?","If we were to write a book together, what would it be about?",
 "If we were to create a YouTube channel, what kind of content would we make?","If we could be any duo from history or fiction, who would we be?",
 "If we could create a new sport, what would the rules be?"],'5 of 300 questions in','Pick one for tonight'),
'wed_random_durian': mc_pin('random','Weird, but true.','What fruit is known as the "king of fruits"?',['Mango','Durian','Pineapple','Papaya'],answer='B'),
'thu_aboutme_dinner': hook_pin('aboutme','Thanksgiving dinner game.','Everyone answers','If you could have dinner with three fictional characters, who would you invite?','One of 300 questions in'),
'fri_parents_gift': note_pin('parents','A gift that is not a gadget.','Black Friday gift idea','Mom and Dad already have everything. Give them 300 questions that turn dinner into stories you will keep.','For Mom, Dad and the grandparents:'),
'fri_memory_gift': note_pin('memory','Gift idea for grandparents.','Large print, no batteries','500 TV, movie, music and sports questions in big type, made for reading aloud at the kitchen table.','A gift they can read aloud:'),
'sat_mazes_gift': note_pin('mazes','Screen-free gift idea.','For grandparents who love puzzles','100 easy mazes in four shapes with solutions included. A calm Christmas gift for grandma and grandpa.','Large print puzzles:'),
'sat_random_list5': list_pin('random','5 quick trivia questions.',[
 'What is a baby kangaroo called?','What is the hardest substance in the human body?','Which planet has a day longer than its year?','What is the smallest bird in the world?','Which bird lays the largest egg?'],'From 300 questions in'),
'sun_memory_list5': list_pin('memory','5 classic music questions.',[
 'Who sang the 1961 hit "Stand By Me"?','What rock band made the album "Hotel California"?','Who is the artist behind "Born to Run"?','Which English musician released "Goodbye Yellow Brick Road"?','Who performed the 1972 hit "Superstition"?'],'From 500 questions in'),
'sun_couples_gift': note_pin('couples','Gift idea for couples.','Date night in a book','300 questions to ask each other over dinner, on a road trip or on the couch. No batteries needed.','Stocking stuffer idea:'),
}
render_pins(P,'../../2026-w48/pins')
