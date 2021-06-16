import spacy
nlp = spacy.load("en_core_web_sm")


class SQuADv1(object):
    def __init__(self, data):
        assert isinstance(data, dict)
        self.examples = self.load(data)

    def __len__(self):
        return len(self.examples)

    def load(self, data):
        examples = []
        for d in data['data']:
            for para in d['paragraphs']:
                c = para['context']
                doc = nlp(c)
                cw = [t.text.lower() for t in doc]
                for qa in para['qas']:
                    q = qa['question']
                    a = qa['answers'][0]['text']
                    qw = [t.text.lower() for t in nlp(q)]
                    n = 0
                    for w in qw:
                        if w in cw:
                            n += 1
                    overlap = n / len(qw)
                    examples.append(SQuADv1Example(c, q, a, qa_id, overlap))
        return examples

class SQuADv1Example(object):
    def __init__(self, context, question, answer, qa_id, overlap):
        self.context = context
        self.question = question
        self.answer = answer
        self.qa_id = qa_id
        self.overlap = overlap
