class Question:
    def __init__(self, q_name, q_text, q_type, q_opts):
        self.q_name = q_name
        self.q_text = q_text
        self.q_type = q_type
        self.q_ans = self.__answer(q_opts)
        self.q_opts = self.__clean_opts(q_opts)

    @staticmethod
    def __answer(opts):
        for k in opts:
            if "_ANSWER_" in opts[k]:
                return k

    @staticmethod
    def __clean_opts(opts):
        for k in opts:
            if "_ANSWER_" in opts[k]:
                opts[k] = opts[k].replace("_ANSWER_", '').strip()
        return opts

    @staticmethod
    def __question_setting(dom):
        shuffle_answers = dom.createElement("shuffleanswers")
        shuffle_answers.appendChild(dom.createTextNode("1"))
        single = dom.createElement("single")
        single.appendChild(dom.createTextNode("true"))
        answer_numbering = dom.createElement("answernumbering")
        answer_numbering.appendChild(dom.createTextNode("none"))
        return shuffle_answers, single, answer_numbering

    def __atr_to_xml(self, dom, elem_name, val, attr=None, is_ans=False):
        elem = dom.createElement(elem_name)
        if attr is not None:
            for key in attr:
                elem.setAttribute(key, attr[key])
        key = dom.createElement("text")
        val = dom.createTextNode(val)
        key.appendChild(val)
        elem.appendChild(key)
        if is_ans:
            feedback = self.__atr_to_xml(dom, "feedback", "Your answer is correct." if attr["fraction"] == "100" else "Your answer is incorrect.")
            elem.appendChild(feedback)
        return elem

    def to_xml(self, dom):
        question = dom.createElement("question")
        question.setAttribute("type", self.q_type)
        name = self.__atr_to_xml(dom, "name", self.q_name)
        questiontext = self.__atr_to_xml(dom, "questiontext", self.q_text, {"format": "html"})
        question.appendChild(name)
        question.appendChild(questiontext)
        for k in self.q_opts.keys():
            answer = self.__atr_to_xml(dom, "answer", self.q_opts[k],
                                       {"fraction": "100"} if self.q_ans == k else {"fraction": "0"}, True)
            question.appendChild(answer)
        # penalty = dom.createElement("penalty")
        # penalty.appendChild(dom.createTextNode("1"))
        if self.q_type == "multichoice":
            q_setting = self.__question_setting(dom)
            question.appendChild(q_setting[0])
            question.appendChild(q_setting[1])
            question.appendChild(q_setting[2])
        return question
