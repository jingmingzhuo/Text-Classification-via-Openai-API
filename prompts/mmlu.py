pure_prompt = """We will ask you a question and you will need to give a direct answer using only A, B, C or D.
Question:{text}
A. {A}
B. {B}
C. {C}
D. {D}
The answer is:"""

cot_prompt = """The following are multiple choice questions (with answers) about world religions.

Q: How can the Upanishads be characterized?
(A) Ritual texts (B) Philosophical texts (C) Hymns (D) Origin stories
A: Let's think step by step. We refer to Wikipedia articles on world religions for help. The Upanishads are the most recent part of Vedas (the oldest scriptures in Hinduism) and supplied the basis of later Hindu philosophy. So they are philosophical texts. The answer is (B).

Q: What is the Second Gem in Buddhism?
(A) The Dharma (B) The Sangha (C) The Buddha (D) The Bodhisattva
A: Let's think step by step. We refer to Wikipedia articles on world religions for help. The Second Gem in Buddhism is The Dharma. The answer is (A).

Q: Which Japanese government promoted a kind of national cult based on the emperor and his associations with kami?
(A) Honen (B) Tanaka (C) Tokugawa (D) Meiji
A: Let's think step by step. We refer to Wikipedia articles on world religions for help. The promotion of a national cult based on the emperor and his associations with Kami happened during the reign of Emperor Meiji (1852-1912). The answer is (D).

Q: In which dynasty was the "Mandate of Heaven" developed to legitimatize the new rulers?
(A) Shang (B) Zhou (C) Han (D) Xia
A: Let's think step by step. We refer to Wikipedia articles on world religions for help. The "Mandate of Heaven" was developed as an ancient Chinese philosophical concept during the Zhou Dynasty (1046-256 BCE). The answer is (B).

Q: What is the sign of the covenant for Jewish males?
(A) The rainbow (B) Circumcision (C) A son (D) Bar mitzvah
A: Let's think step by step. We refer to Wikipedia articles on world religions for help. In Judaism, the most distinctive sign of the covenant is circumcision (brit milah). The answer is (B).

Q:{text}
(A){A} (B){B} (C){C} (D){D}
A: Let's think step by step. """

proposal_prompt = """The following are multiple choice questions (with answers) about world religions.

Question: How can the Upanishads be characterized?
A. Ritual texts 
B. Philosophical texts 
C. Hymns 
D. Origin stories
Let's think step by step: We refer to Wikipedia articles on world religions for help. The Upanishads are the most recent part of Vedas (the oldest scriptures in Hinduism) and supplied the basis of later Hindu philosophy. So they are philosophical texts.
The answer is: B.

Question: What is the Second Gem in Buddhism?
A. The Dharma
B. The Sangha
C. The Buddha
D. The Bodhisattva
Let's think step by step: We refer to Wikipedia articles on world religions for help. The Second Gem in Buddhism is The Dharma.
The answer is: A.

Question: Which Japanese government promoted a kind of national cult based on the emperor and his associations with kami?
A. Honen
B. Tanaka
C. Tokugawa
D. Meiji
Let's think step by step: We refer to Wikipedia articles on world religions for help. The promotion of a national cult based on the emperor and his associations with Kami happened during the reign of Emperor Meiji (1852-1912).
The answer is: D.

Question: In which dynasty was the "Mandate of Heaven" developed to legitimatize the new rulers?
A. Shang
B. Zhou
C. Han
D. Xia
Let's think step by step: We refer to Wikipedia articles on world religions for help. The "Mandate of Heaven" was developed as an ancient Chinese philosophical concept during the Zhou Dynasty (1046-256 BCE).
The answer is: B.

Question: What is the sign of the covenant for Jewish males?
A. The rainbow
B. Circumcision
C. A son
D. Bar mitzvah
Let's think step by step: We refer to Wikipedia articles on world religions for help. In Judaism, the most distinctive sign of the covenant is circumcision (brit milah).
The answer is: B.

Question: {text}
A. {A}
B. {B}
C. {C}
D. {D}
Let's think step by step: 
"""

vote_prompt = """Given an question and several thoughts, decide which thoughts is most promising. Analyze each thought in detail, then conclude in the last line "The best thought is n", where n is the integer id of the thought.

Question: {text}

"""

after_tot_prompt = """The following are multiple choice questions (with answers) about world religions.

Question: How can the Upanishads be characterized?
A. Ritual texts 
B. Philosophical texts 
C. Hymns 
D. Origin stories
Let's think step by step: We refer to Wikipedia articles on world religions for help. The Upanishads are the most recent part of Vedas (the oldest scriptures in Hinduism) and supplied the basis of later Hindu philosophy. So they are philosophical texts.
The answer is: B.

Question: What is the Second Gem in Buddhism?
A. The Dharma
B. The Sangha
C. The Buddha
D. The Bodhisattva
Let's think step by step: We refer to Wikipedia articles on world religions for help. The Second Gem in Buddhism is The Dharma.
The answer is: A.

Question: Which Japanese government promoted a kind of national cult based on the emperor and his associations with kami?
A. Honen
B. Tanaka
C. Tokugawa
D. Meiji
Let's think step by step: We refer to Wikipedia articles on world religions for help. The promotion of a national cult based on the emperor and his associations with Kami happened during the reign of Emperor Meiji (1852-1912).
The answer is: D.

Question: In which dynasty was the "Mandate of Heaven" developed to legitimatize the new rulers?
A. Shang
B. Zhou
C. Han
D. Xia
Let's think step by step: We refer to Wikipedia articles on world religions for help. The "Mandate of Heaven" was developed as an ancient Chinese philosophical concept during the Zhou Dynasty (1046-256 BCE).
The answer is: B.

Question: What is the sign of the covenant for Jewish males?
A. The rainbow
B. Circumcision
C. A son
D. Bar mitzvah
Let's think step by step: We refer to Wikipedia articles on world religions for help. In Judaism, the most distinctive sign of the covenant is circumcision (brit milah).
The answer is: B.

Question: {text}
A. {A}
B. {B}
C. {C}
D. {D}
Let's think step by step: {thoughts}
The answer is: 
"""