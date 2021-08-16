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
                for qa in para['qas']:
                    q = qa['question']
                    a = qa['answers'][0]['text']
                    qa_id = qa['id']
                    examples.append(SQuADv1Example(c, q, a, qa_id))
        return examples

class SQuADv1Example(object):
    def __init__(self, context, question, answer, qa_id):
        self.context = context
        self.question = question
        self.answer = answer
        self.qa_id = qa_id
