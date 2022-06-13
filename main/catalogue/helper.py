class Helper:
    def remove_space(val):
        if(val):
            return val.replace(" ", "")
        else: return None
    def number_prefix(n):
        if len(str(n)) == 1:n = '00' + str(n)
        elif len(str(n)) == 2:n = '0' + str(n)
        else: n = str(n)
        return n