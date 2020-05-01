Запуск в режиме подсчета вероятностей
 python3 main.py calculate_probabilities text.txt probs.pickle 3


Запуск в режиме генерации:
 python3 main.py generate_text probs.pickle 3 300 --output_file generated.txt
* Если не указать output_file в режиме генерации, то выведет текст в стандартный поток


Примеры генерации (оба исходных текста лежат в корне репозитория).

На основе Алисы в стране чудес на английском:

Пример 1 с глубиной 3:

Alice did not like to be a walrus or hippopotamus, but I think I can find them. However, I've had such a thing before, but it doesn't understand English, who was trembling down to them, but it just grazed his nose, and the other, and the Queen said to herself, for she had not gone much further before she came upon a neat little house, and the little door about fifteen inches high, and she tried to fancy what the next witness would be as well as she could, for she was quite out of sight, they all spoke at once, while the rest of the court. 

All persons more than that. Then she set to work very carefully, remarking, as she could not, could not, could not think of any one left alive! I think you'd take a fancy to cats, or at any rate, the Queen. First, she found herself in a low voice, and was going on, without knowing how old it was, that the Queen, and she tried to curtsey as she could, for she felt that this might belong to one of the house before she had never been so much! 


Пример 2 (с глубиной 7):

The Queen turned angrily away from him, and said to the Knave, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried. The poor little thing was snorting like a steam-engine when she caught it, and kept doubling itself up and straightening itself out again, so that altogether, for the first minute or two, it was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again. 

Alice waited a little, half expecting to see it again, but it did not appear, and after a minute or two she walked on in the direction in which the March Hare was said to live. The Hatter shook his head mournfully. The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back. However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more. 


На основе Алисы в стране чудес на русском ( http://lib.ru/CARROLL/alisa_zah.txt ):

Пример 1 (с глубиной 3):

Алиса в восторге, но она все-таки немножко удивиться стоило, но, к счастью, она не знала, что, если все не будет исполнено сию секунду и даже заглянула ему пол шляпку, а потом. Алиса была так напугана, что это всего-навсего ПРЕДИСЛОВИЕ! Алиса глядела во все глаза, и Алиса закричала изо всех сил встряхивая бедняжку в конце концов отважилась откусить - совсем чуточку! И все присутствующие тупо молчали. Едва показалась Алиса, а не та, знаменитая. И все почему-то безголовые. Алиса была так ошеломлена, что это такое, но, когда я его не сегодня! 

И тут все захлопали и закричали "Ура"! Голова на воле! Алиса была вне себя от ужаса. Алиса была умная девочка и опять исчез. Не прошло и пяти минут, как вдруг заметила в воздухе какое-то странное явление. Сначала она чуточку робела - уж очень ей стало печально и одиноко, что я могу сказать! И она принялась рассказывать обо всем этом подумаете вы. Алиса не знала, что я вас (совсем немножко: как раз, когда я встала, я бы ни за какие тысячи не расстался - такой наряд был ему явно не к лицу). 


Пример 2 (с глубиной 7): 

И она заговорила: он стукнулся об ее собственные ботинки! Как ни ошеломлена была Алиса, она все же сообразила, что времени терять нельзя: надо немедленно откусить хоть чуточку от другого куска, иначе она пропала! Не успела Алиса выпить и половины, как упилась головой в потолок, и ей пришлось сильно наклониться, чтобы не сломать себе шею. Она поскорее поставила его обратно, приговаривая: она сама почувствовала, что слово какое-то не совсем такое. Грифон фыркнул. Алиса была так напугана, что не произнесла ни слова и молча поплелась за Королевой на крокетную площадку. 

Остальные игроки, воспользовавшись отсутствием ее величества, расположились на отдых в тени, но едва она показалась, как они немедленно возобновили игру. Промедление было смерти подобно - Королева мимоходом заметила, что кто хоть чуточку опоздает, будет казнен без опоздания. Игра пошла по-прежнему: Королева не переставала со всеми спорить, скандалить и кричать: она была уверена, что если не просохнет очень скоро, то непременно схватит ужасный насморк. И она решила подождать. Грифон приподнялся, сел и протер глаза; он долго смотрел вслед Королеве, а когда она окончательно скрылась из виду, фыркнул. 

