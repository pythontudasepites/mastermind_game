from __future__ import annotations
import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from enum import Enum
from mastermind_model import Game, GameState
from itertools import product

MAX_ROWCOUNT = 12  # A tippsorok maximális száma.
CELL_SIDE_SIZE = 50  # A színjelzőket tartalmazó táblázatrácsban a négyzet alakú cell oldalmérete.
BASE_COLOR = 'brown4'  # A játéktábla alapszíne.
# A játékban szereplő hat szín és az üres pozíció színe.
Color = Enum('Color', dict(Magenta='#ff00ff', Green='#00ff00', Blue='#0000ff', Yellow='#ffff00', White='#ffffff',
                           Black='#000000', Empty='#bfbfbf'))


class HiddenCodesPanel(tk.Frame):
    """Az elrejtett kódokat (színeket) tartalmazó területet megvalósító rész."""

    def __init__(self, master: MastermindGame):
        super().__init__(master)
        cell_side = CELL_SIDE_SIZE
        # A színjelzőket tartalmazó négy cellát egy-egy vászon elem valósítja meg, amelyen egy kirajzolt kör a színjelző alakzat.
        for ci in range(4):
            cnv = tk.Canvas(self, width=cell_side, height=cell_side, highlightthickness=0, relief=tk.SUNKEN, bd=2, bg=BASE_COLOR)
            cnv.create_oval(cell_side / 4, cell_side / 4, cell_side * 3 / 4, cell_side * 3 / 4,
                            fill=BASE_COLOR, width=0, tags='hiddencodepeg')
            cnv.grid(row=0, column=ci)  # A vászon elemek lehelyezése.

    def set_codepeg_colors(self, color_codes: list[str]):
        """Az argumentum sorrendben tartalmazza a színkódokat, amelyek az egyes színjelző körök kitöltőszínei lesznek."""
        for cnv, color_code in zip(self.winfo_children(), color_codes):
            cnv.itemconfig('hiddencodepeg', fill=color_code)

    def hide_codepegs(self):
        """A színjelző körök színeinek elrejtése a kitöltőszínük alapszínre állításával."""
        for cnv in self.winfo_children():
            cnv.itemconfig('hiddencodepeg', fill=BASE_COLOR)


class DecodingBoard(tk.Frame):
    """A tippelőtábla (dekódoló tábla) területet megvalósító rész."""

    def __init__(self, master: MastermindGame, rowcount):
        super().__init__(master)
        # A játékban szereplő színeket sorrendben eltároljuk és azonosítószámokat rendelünk hozzájuk a későbbi könnyebb kezeléshez.
        self.colors = (Color.Empty.value, Color.Magenta.value, Color.Green.value, Color.Blue.value, Color.Yellow.value,
                       Color.White.value, Color.Black.value)
        self.colors_codevalues = dict(zip(self.colors, range(7)))
        # A színjelzőket tartalmazó, soronként négy cellát egy-egy vászon elem valósítja meg, amelyen egy kirajzolt kör a színjelző alakzat.
        cell_side = CELL_SIDE_SIZE
        for ri, ci in product(range(rowcount), range(4)):
            cnv = tk.Canvas(self, width=cell_side, height=cell_side, bg=BASE_COLOR, highlightthickness=0, relief=tk.SUNKEN, bd=2)
            cnv.create_oval(cell_side / 4, cell_side / 4, cell_side * 3 / 4, cell_side * 3 / 4, fill=Color.Empty.value, tags='codepeg')
            cnv.grid(row=ri, column=ci)  # A vászon elemek lehelyezése.
            # A kör rajzelemhez a bal egérgomb kattintás esemény és a kör színét változtató eseménykezelő rendelése.
            cnv.tag_bind('codepeg', '<Button 1>', self.change_color)
            # A találatjelzőket tartalmazó négyzet alakú grafikus elem elhelyezése a tippsor végén.
        for ri in range(rowcount):
            KeyPegsPanel(self).grid(row=ri, column=4)

    def change_color(self, event) -> None:
        """Megváltoztatja az aktuális tippsorban az eseménnyel érintett vásznon levő kör rajzelem kitöltőszínét a színsorozatban szereplő
        következő színre körkörös módon. Vagyis, ha a sorozat utolsó színéhez ér, akkor a következő szín a sorozat első színe lesz.
        """
        cnv: tk.Canvas = event.widget
        # Színváltoztatás csak az aktuális tippsorban lehetséges. Vagyis akkor, ha a nyilvántartott aktuális sorindex megegyezik azon
        # rács-sorindexszel, amely sorban az eseménnyel érintett vászon elem van.
        if self.master.game.current_row_index == cnv.grid_info()['row']:
            # Az aktuális sorban levő, eseménnyel érintett kör színe.
            current_color = cnv.itemcget('current', 'fill')
            # Az aktuális szín indexe a színsorozatban.
            index = self.colors.index(current_color)
            # A kör kitöltőszínének változtatása a sorban következő színre körkörös módon.
            cnv.itemconfig('current', fill=self.colors[(index + 1) % len(self.colors)])

    def get_colorcodes_in_current_row(self) -> list[str]:
        """Egy olyan listával tér vissza, amelynek elemei az aktuális sorban levő körök színkódjai."""
        return [widget.itemcget('codepeg', 'fill')
                for ci in range(4)
                for widget in self.grid_slaves(row=self.master.game.current_row_index, column=ci)
                if type(widget) is tk.Canvas]

    def disable_all_codepegs(self) -> None:
        """A tipptábla összes színjelölő körét eseményekre érzéketlenné teszi."""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.tag_unbind('codepeg', '<Button 1>')


class KeyPegsPanel(tk.Frame):
    """A találatjelzőket tartalmazó területet megvalósító rész."""

    def __init__(self, master: DecodingBoard):
        super().__init__(master)
        cell_side = CELL_SIDE_SIZE
        # Vászon elem létrehozása, amin a négy, köralakú találatjelző kirajzolódik.
        self.cnv = tk.Canvas(self, width=cell_side, height=cell_side, bg='green', highlightthickness=0, bd=2, relief=tk.SUNKEN)
        self.circle_ids = []  # A kör rajzelemek azonosítóinak listája.
        r = cell_side / 8  # A kör rajzelemek sugara.
        # Kör rajzelemek létrehozása a vásznon szimmetrikus elrendezésben egy négyzet csúcsaiként.
        for dx, dy in [(0, 0), (cell_side / 2, 0), (0, cell_side / 2), (cell_side / 2, cell_side / 2)]:
            circle_id = self.cnv.create_oval(cell_side / 4 + dx - r, cell_side / 4 + dy - r,
                                             cell_side / 4 + dx + r, cell_side / 4 + dy + r, fill=Color.Empty.value, tags='keypeg')
            self.circle_ids.append(circle_id)
        self.cnv.grid(row=0, column=0, padx=0, pady=0)  # A vászon elem lehelyezése.

    def set_keypeg_colors(self, blackcount: int, whitecount: int):
        """A találatjelzők színeinek beállítása az argumentumban kapott találatok alapján, ahol a blackcount a pozícióban is helyes
        találatok számát jelzi, a whitecount pedig azokat, amelyek bár szerepelnek a rejtett kódban, de nem a helyes pozícióban.
        """
        for circle_id in self.circle_ids[0:blackcount]:
            self.cnv.itemconfig(circle_id, fill=Color.Black.value)
        for circle_id in self.circle_ids[blackcount:4][0:whitecount]:
            self.cnv.itemconfig(circle_id, fill=Color.White.value)


class ControlPanel(tk.Frame):
    """A játékopciók beállítását lehetővé tevő és a játék funkciógomjait tartalmazó területet megvalósító rész."""

    def __init__(self, master: MastermindGame):
        super().__init__(master)
        # Grafikus elemek létrehozása.
        # Az aktuális sorban szereplő tipp ellenőrzését indító nyomógomb.
        check_btn = tk.Button(self, text='TIPP ELLENŐRZÉS', font=('Arial', 12, 'bold'), bg='gray50', fg='white',
                              command=self.master.check_guess)
        # Tippsorok számának meghatározásához bevíteli mező és a hozzá tartozó címke.
        lbl_ent = tk.Label(self, text='Tippsorok száma:', font=('Arial', 12), anchor='w')
        self.rowcount_var = tk.IntVar(value=self.master.rowcount)
        ent_rowcount = tk.Entry(self, textvariable=self.rowcount_var, font=('Arial', 14, 'bold'), width=4, justify=tk.CENTER)
        # Jelölőnégyzetek a színismétlődés és/vagy az üres pozíció rejtett kódként szerepeltetésének engedélyezésére vagy tiltására.
        self.chb_empty_allowed_var = tk.BooleanVar(value=False)
        chb_empty_allowed = tk.Checkbutton(self, text='Üres pozíció is számít', variable=self.chb_empty_allowed_var, font=('Arial', 12))
        self.chb_repetition_allowed_var = tk.BooleanVar(value=False)
        chb_repetition_allowed = tk.Checkbutton(self, text='Színek ismétlődése megengedett', variable=self.chb_repetition_allowed_var,
                                                font=('Arial', 12))

        def new_game():
            """A beállított opciókkal új játékot indít, ha a beállított tippsorok száma nem nagyobb a megengedettnél.
            Ha nagyobb, akkor erről egy felugró üzenetablak tájékoztat.
            """
            if self.rowcount_var.get() in range(1, MAX_ROWCOUNT + 1):
                self.master.new_game_with_current_settings()
            else:
                showerror('Mastermind játék'.upper(), f'A tippsorok száma 1 és {MAX_ROWCOUNT} között lehet!'.upper())

        # A beállított opciókkal új játék indítását lehetővé tevő nyomógomb.
        btn_new_play = tk.Button(self, text='új játék'.upper(), font=('Arial', 12, 'bold'), bg='gray80', command=new_game)

        # Grafikus elemek táblázatos lehelyezése.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=25)

        check_btn.grid(row=0, column=0, columnspan=2, sticky='we')
        lbl_ent.grid(row=1, column=0, sticky='w', pady=(10, 0))
        ent_rowcount.grid(row=1, column=1, sticky='w', pady=(10, 0))
        chb_empty_allowed.grid(row=2, column=0, columnspan=2, sticky='w', pady=(10, 0))
        chb_repetition_allowed.grid(row=3, column=0, columnspan=2, sticky='w', pady=(2, 5))
        btn_new_play.grid(row=4, column=0, columnspan=2, sticky='we')


class MastermindGame(tk.Tk):
    """A játék egyes komponens területeiből a játéktáblát összeállítja és a vezérli a játékmenetet."""

    def __init__(self, rowcount=8, empty_hole_allowed=False, repetition_allowed=False):
        super().__init__()
        self.title('Mastermind játék'.upper())
        self.resizable(False, False)
        self.rowcount, self.empty_hole_allowed, self.repetition_allowed = rowcount, empty_hole_allowed, repetition_allowed
        # A komponens területeket megvalósító példányok létrehozása és lehelyezése.
        self.hidden_codes_panel = HiddenCodesPanel(self)
        self.decoding_board = DecodingBoard(self, rowcount=self.rowcount)
        self.button_panel = ControlPanel(self)

        self.hidden_codes_panel.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.decoding_board.grid(row=1, column=0, padx=5, pady=0, sticky='w')
        self.button_panel.grid(row=2, column=0, sticky='news', padx=5, pady=5)
        # A játék logikai részét, modelljét megvalósító objektum létrehozása a megadott paraméterbeállításokkal.
        self.game = Game(rowcount=self.rowcount, empty_hole_allowed=self.empty_hole_allowed, repetition_allowed=self.repetition_allowed)
        self.game.hide_pegs()  # Az elrejtendő kódok generálása.

    def new_game_with_current_settings(self):
        """Új játék kezdése az aktuálisan beállított opciók értékeivel."""
        self.hidden_codes_panel.hide_codepegs()  # A rejtett kódokat tartalmaző terület elfedése.
        # Az eddigi tipptábla törlése és egy új létrehozása az aktuálisan érvényes számú sorral, majd lehelyezése.
        self.decoding_board.destroy()
        self.decoding_board = DecodingBoard(self, rowcount=self.button_panel.rowcount_var.get())
        self.decoding_board.grid(row=1, column=0, padx=5, pady=0)
        # A játék logikai részének, modelljének aktualizálása és az elrejtendő kódok generálása.
        self.game = Game(rowcount=self.button_panel.rowcount_var.get(), empty_hole_allowed=self.button_panel.chb_empty_allowed_var.get(),
                         repetition_allowed=self.button_panel.chb_repetition_allowed_var.get())
        self.game.hide_pegs()

    def check_guess(self):
        """Az aktuális sorban levő tipp kiértékelése a modell alapján, és az eredménynek megfelelő visszajelzés."""
        codepeg_colors_in_current_row = self.decoding_board.get_colorcodes_in_current_row()
        code_values = tuple(map(self.decoding_board.colors_codevalues.get, codepeg_colors_in_current_row))
        self.game.next_guess(*code_values)
        black_pegs, white_pegs = self.game.check_guess()
        keypegspanel_in_current_row = self.decoding_board.grid_slaves(row=self.game.current_row_index, column=4)[0]
        keypegspanel_in_current_row.set_keypeg_colors(black_pegs, white_pegs)
        self.game.check_state()
        # Ha a modell szerint a játék befejeződött, akkor a a rejtett kódok felfedése, a sikeresség eldöntése és ennek megfelelő
        # visszajelzés, valamint a tipptábla összes színjelölő köre módosíthatóságának letiltása.
        if self.game.state != GameState.GUESSING:
            hidden_colors = [colorcode for hidden_code in self.game.hidden_codes
                             for colorcode, color_codevalue in self.decoding_board.colors_codevalues.items()
                             if hidden_code == color_codevalue]
            self.hidden_codes_panel.set_codepeg_colors(hidden_colors)
            if self.game.state == GameState.WON:
                showinfo('MASTERMIND EREDMÉNY', '{:20}'.format('HELYES MEGOLDÁS!'))
            elif self.game.state == GameState.LOST:
                showinfo('MASTERMIND EREDMÉNY', '{:20}'.format('EZ MOST NEM SIKERÜLT!'))
            self.decoding_board.disable_all_codepegs()

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    MastermindGame().run()
