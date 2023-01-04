class LangHandler:

    def __init__(self, cur_lang = "en_US"):
        self.cur_lang = cur_lang
        self.cur_lang_data = self.gt_pack_data(self.cur_lang)
        self.errors = self.gt_pack_data("errors", "resources")

    def gt_pack_data(self, pack, dir = "language packs"):
        return dict(eval(self.gt_pack_str(pack, dir)))

    def gt_pack_str(self, pack, dir):
        try:
            with open(f"{dir}/{pack}.txt", "r", encoding = "utf-8") as file:
                return file.read()
        except:
            if dir == "language packs":
                raise FileNotFoundError("Couldn't fetch language pack '" + pack + "'.")
            else:
                raise FileNotFoundError("Couldn't fetch data pack '" + pack + "'.")

    def demo(self):
        try:
            demo = self.cur_lang_data["demo"]
        except:
            raise FileNotFoundError("Couldn't fetch demo data from language pack '" + self.cur_lang + "'.")
        return demo

    def abt_win(self, key):
        try:
            ele = self.cur_lang_data["abt_win"][key]
        except:
            raise FileNotFoundError("Couldn't fetch 'about' window data for '" + key + "' from language pack '" + self.cur_lang + "'.")
        return ele

    def shc_win(self, key):
        try:
            ele = self.cur_lang_data["shc_win"][key]
        except:
            raise FileNotFoundError(f"Couldn't fetch 'shortcuts' window data for '{key}' from language pack '{self.cur_lang}'.")
        return ele

    def ver_win(self, key, **kwargs):
        try:
            ele = self.cur_lang_data["ver_win"][key]
        except:
            raise FileNotFoundError(f"Couldn't fetch 'version_error' window data for '{key}' from language pack '{self.cur_lang}'.")
        if key == "text":
            text = ""
            blocks = ele.split("}")
            if len(blocks) == 1:
                text = blocks[0]
            else:
                for i in range(len(blocks) - 1):
                    txt_arg_pair = blocks[i].split("{", maxsplit=1)
                    if len(txt_arg_pair) == 1:
                        raise SyntaxError(f"Unmatched curly bracket in error data for '{err}'.")
                    else:
                        arg = None
                        for kw in kwargs:  # search for matching argument
                            if kw == txt_arg_pair[1]:
                                arg = kwargs[kw]
                        if arg == None:
                            raise TypeError(f"LangHandler.ver_win() missing required keyword argument '{txt_arg_pair[1]}' in 'version_error' window data for '{key}' from language pack '{self.cur_lang}'.")
                        text += txt_arg_pair[0] + str(arg[0]) + "." + str(arg[1])
                text += blocks[len(blocks) - 1]
            return text
        return ele

    def gui(self, key):
        try:
            ele = self.cur_lang_data["gui"][key]
        except:
            raise FileNotFoundError(f"Couldn't fetch gui data for '{key}' from language pack '{self.cur_lang}'.")
        return ele

    def file_mng(self, key):
        try:
            ele = self.cur_lang_data["file_mng"][key]
        except:
            raise FileNotFoundError(f"Couldn't fetch file_mng data for '{key}' from language pack '{self.cur_lang}'.")
        return ele

    def asm_win(self, key):
        try:
            ele = self.cur_lang_data["asm_win"][key]
        except:
            raise FileNotFoundError(f"Couldn't fetch 'Assembly' window data for '{key}' from language pack '{self.cur_lang}'.")
        if key == "text":
            text_code_pairs = []
            blocks = ele.split("}")
            if len(blocks) == 1:
                text_code_pairs = [(blocks[0], "")]
            else:
                for i in range(len(blocks) - 1):
                    text_code_pair = blocks[i].split("{", maxsplit = 1)
                    if len(text_code_pair) == 1:
                        raise SyntaxError(f"Unmatched curly bracket in 'Assembly' window data for 'text' from language pack '{self.cur_lang}'.")
                    else:
                        text_code_pairs.append(text_code_pair)
                text_code_pairs.append((blocks[len(blocks) - 1], ""))
            return text_code_pairs
        return ele

    def error(self, err, **kwargs):
        try:
            err_tpl = self.errors[err]
        except:
            raise FileNotFoundError(f"Couldn't fetch error data for '{err}'.")
        err_name = err_tpl[0]
        err_desc = ""
        blocks = err_tpl[1].split("}")
        if len(blocks) == 1:
            err_desc = blocks[0]
        else:
            for i in range(len(blocks) - 1):
                txt_arg_pair = blocks[i].split("{", maxsplit = 1)
                if len(txt_arg_pair) == 1:
                    raise SyntaxError(f"Unmatched curly bracket in error data for '{err}'.")
                else:
                    arg = None
                    for kw in kwargs: # search for matching argument
                        if kw == txt_arg_pair[1]:
                            arg = kwargs[kw]
                    if arg == None:
                        raise TypeError(f"LangHandler.error() missing required keyword argument '{txt_arg_pair[1]}' in error data for '{err}'.")
                    err_desc += txt_arg_pair[0] + str(arg)
            err_desc += blocks[len(blocks) - 1]
        return err_name + ": " + err_desc