#!/usr/bin/env python3

from tkinter import tix
from tkinter.simpledialog import askstring


BAREME = dict((
((2,0),4),
((2,1),3),
((1,1),2),
((1,2),2),
((0,2),1),
))


class Player :

    __slots__ = ["name", "score"]

    players = dict()

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.players[self.name] = self
    def __iadd__(self, value):
        self.score += value
        return self
    def __repr__(self):
        return "{} ({} pts)".format(self.name, self.score)
    __str__ = __repr__


class App :

    def __init__(self):
        self.main = tix.Tk()
        self.leftpane = tix.ScrolledListBox(self.main)

        self.register = tix.Button(self.main, text="Nouveau joueur", command=self.add_player)
        self.match = tix.Button(self.main, text="Nouveau match", command=self.new_match)

        self.leftpane.pack(side="left",fill="y")
        self.register.pack(side="top", fill="x")
        self.match.pack(side="bottom", fill="x")

        self.players = list()

    def add_player(self):
        name = askstring("Nouveau joueur", "Nom du nouveau joueur :")
        if name is not None :
            self.players.append(Player(name))
            self.sort()

    def new_match(self):
        tl = tix.Toplevel(self.main)
        p1,p2 = tix.ComboBox(tl),tix.ComboBox(tl)
        score_p1, score_p2 = tix.Entry(tl), tix.Entry(tl)
        ok = tix.Button(tl, text="OK",
                command=lambda : self._process(
                    p1=p1, p2=p2, score_p1=score_p1, score_p2=score_p2, tl=tl
                ))
        names = [pl.name for pl in self.players]
        p1.slistbox.listbox.insert(0, *names)
        p2.slistbox.listbox.insert(0, *names)

        p1.grid(row=0,column=0)
        score_p1.grid(row=0,column=1)
        tix.Label(tl,text=" - ").grid(row=0,column=2)
        score_p2.grid(row=0,column=3)
        p2.grid(row=0,column=4)
        ok.grid(row=1, column=2)

    def _process(self, *, p1, p2, score_p1, score_p2, tl):
        p1 = Player.players[p1["value"]]
        p2 = Player.players[p2["value"]]
        score_p1 = int(score_p1.get())
        score_p2 = int(score_p2.get())
        tl.destroy()
        p1 += BAREME[(score_p1, score_p2)]
        p2 += BAREME[(score_p2, score_p1)]

        self.sort()

    def sort(self):
        self.players.sort(key=lambda player:player.score, reverse=True)
        self.leftpane.listbox.delete(0, "end")
        self.leftpane.listbox.insert(0, *self.players)


if __name__ == '__main__':
    app = App()
    app.main.mainloop()
