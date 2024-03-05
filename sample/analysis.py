class Analysis:
    def __init__(self, title, data):
        self.title = title
        self.data = data

    def fstr(f):
        return str(round(f, 2))
    
    def prettier(self, depth=0):
        str = ""
        for title in self.data.keys():
            curr = self.data[title]
            for i in range(depth):
                str += "\t"

            if isinstance(curr, dict):
                str += title + ":\n" + self.prettier(curr, depth+1)
            else:
                str += title + ": "
                
                if isinstance(curr, list):
                    str += "["
                    for i in range(len(curr) - 1):
                        str += self.fstr(curr[i]) + ", "
                    str += self.fstr(curr[i+1]) + "]\n"
                else:
                    str += self.fstr(curr) + "\n"

        str += "\n"

        return str
    

