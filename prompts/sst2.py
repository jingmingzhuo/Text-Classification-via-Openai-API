pure_prompt = """Given a movie review, please tell me if the review is positive or negative.
Comments: {text}
This movie is: 
"""

few_shot_prompt = """Given a movie review, please tell me if the review is positive or negative.

Comments: it 's a charming and often affecting journey .
This movie is: positive.

Comments: unflinchingly bleak and desperate
This movie is: negative.

Comments: allows us to hope that nolan is poised to embark a major career as a commercial yet inventive filmmaker .
This movie is: positive.

Comments: the acting , costumes , music , cinematography and sound are all astounding given the production 's austere locales .
This movie is: positive.

Comments: the acting , costumes , music , cinematography and sound are all astounding given the production 's austere locales . 	1
it 's slow -- very , very slow .
This movie is: negative.

Comments: {text}
This movie is: 
"""