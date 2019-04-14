import re


class QuizRangliste:
    """
    stellt ein QuizRangliste Objekt her
    """

    def __init__(self, datei):
        """
        Konstruktor fuer Klassenelementen
        """
        self._data = ''
        self._file = datei
        _regex = re.compile(r"\w+,[0-9]+,[0-9]+\.[0-9]+")
        with open(datei, 'r') as f:
            for line in f:
                if _regex.match(line):
                    self._data += line

    def als_dictionary(self):
        """
        Gibt intern gespeicherte Dateien als Dictionary
        von Dictionaries wieder zurueck
        """
        _dict_ = {}
        for line in iter(self._data.splitlines()):
            _ = line.partition(',')
            _1 = _[2].partition(',')
            _dict_.update({_[0]: {'Punkte': int(_1[0]),
                                  'Zeit': float(_1[2])}})
        return _dict_

    def als_liste(self):
        """
        Gibt intern gespeicherte Dateien als Liste wieder zurueck
        """
        _list_ = []
        for line in iter(self._data.splitlines()):
            _ = line.partition(',')
            _1 = _[2].partition(',')
            _list_ += [(_[0], int(_1[0]), float(_1[2]))]
        return sorted(_list_, key=lambda x: (-x[1], x[2], x[0]))

    def als_string(self):
        """
        Gibt intern gespeicherte Dateien als String wieder zurueck
        """
        _str_ = ''
        _list_ = []
        _length_list_ = []
        for line in iter(self._data.splitlines()):
            _ = line.partition(',')
            _1 = _[2].partition(',')
            _list_ += [(_[0], int(_1[0]), float(_1[2]))]
        _list_ = sorted(_list_, key=lambda x: (-x[1], x[2], x[0]))
        for name in _list_:
            _length_list_ += [(len(str(name[0])), len(str(name[1])),
                               len(str(name[2])))]
        _max0 = max(_length_list_, key=lambda x: x[0])[0]
        _max1 = max(_length_list_, key=lambda x: x[1])[1]
        _max2 = max(_length_list_, key=lambda x: x[2])[2]
        for name in _list_:
            _str_ += name[0].ljust(_max0+1) + "|" + \
                     str(name[1]).rjust(_max1+1) + " |" + \
                     str(name[2]).rjust(_max2+1) + "\n"
        return _str_

    def resultat_addieren(self, name, punkte, zeit):
        """
        Addiert Punkte und Zeit zu einem bereits Eintrag
        name(str), punkte(str oder int), zeit(str oder float)
        """
        _name_is_in = 0
        lines = self._data.splitlines()
        for i, line in enumerate(lines):
            _ = line.partition(',')
            if _[0] == name:
                _name_is_in = 1
                _1 = _[2].partition(',')
                _alte_punkte = int(_1[0])
                _alte_zeit = float(_1[2])
                _neue_punkte = _alte_punkte + int(punkte)
                _neue_zeit = _alte_zeit + float(zeit)
                lines[i] = _[0] + ',' + str(_neue_punkte) + \
                    ',' + str(_neue_zeit)
        if _name_is_in == 1:
            self._data = '\n'.join(lines)
        else:
            self._data += '\n'+name+','+str(punkte)+','+str(zeit)

    def name_entfernen(self, name):
        '''
        Entfernt einen Eintrag aus den internen Dateien
        '''
        lines = self._data.splitlines()
        lines = tuple(x for x in lines if x.partition(',')[0] != name)
        self._data = '\n'.join(lines)

    def speichern(self, als=None):
        '''
        Speichert interne Dateien als ein txt File
        '''
        if als is None:
            with open(self._file, 'w') as f:
                f.write(self._data)
        else:
            with open(als, 'w') as f:
                f.write(self._data)
