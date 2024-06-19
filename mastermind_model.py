import operator as op
from collections import Counter
from random import sample, choices
from enum import IntEnum


class GameState(IntEnum):
    """A sikertelenül véget ért, a folyamatban levő, valamint a helyes megoldással végződő játékállapotokat jelző konstansok."""
    LOST = -1
    GUESSING = 0
    WON = +1


class Game:
    """A Mastermind játék logikai modelljét képviselő osztály"""

    def __init__(self, rowcount=8, empty_hole_allowed=False, repetition_allowed=False):

        self.rowcount = rowcount  # A tippsorok száma.
        self.empty_hole_allowed = empty_hole_allowed  # Az üres pozíció szerepelhet-e mint rejtett kód.
        self.repetition_allowed = repetition_allowed  # A rejtett kódok között lehet-e ismétlődés.
        # Az elrejtendő kódok lehetséges értékei, ha az üres pozíció nem játszik: 1..6. Ha az üres pozíció is számít akkor 0..6.
        self.codepeg_values = tuple(range(0, 7)) if empty_hole_allowed else tuple(range(1, 7))
        # Az elrejtett kódokat tartalmazó négyelemű lista.
        self.hidden_codes = [0] * 4
        # Az aktuális tippsort nyilvántartó változó.
        self.current_row_index = 0
        # Az aktuális tippsor kódértékeit tartalmazó négyelemű lista.
        self.current_guess = [0] * 4
        # Az aktuális tippsorban a találatok darabszámát tároló változók. A black_pegs a pozícióban is helyes találatok számát jelzi, a
        # white_pegs pedig azokat, amelyek bár szerepelnek a rejtett kódban, de nem a helyes pozícióban.
        self.black_pegs = self.white_pegs = 0
        # A játék állapota induláskor.
        self.state = GameState.GUESSING

    def hide_pegs(self) -> None:
        """Az elrejtendő kódok generálása és eltárolása."""
        # Véletlenszerűen kiválasztunk 4-et a megengedett kódértékek tartományából.
        if self.repetition_allowed:
            self.hidden_codes = choices(self.codepeg_values, k=4)
        else:
            self.hidden_codes = sample(self.codepeg_values, k=4)

    def next_guess(self, *guess) -> None:
        """Az aktuális kódtippek eltárolása."""
        self.current_guess[:] = guess

    def check_guess(self) -> tuple[int, int]:
        """Az aktuális tipp kiértékelése. Ennek eredménye, hogy hány olyan találat van, amelyek pozícióban is helyesek, és
        mennyi az, ahol van találat, de a pozíció nem jó.
        """
        # Annak száma, ahány esetben a tippelt kódérték helyes.
        code_matches = len(Counter(self.hidden_codes) & Counter(self.current_guess))
        # Azon jelzők száma, ahány esetben a kódérték és a pozíció is helyes.
        black_pegs = [*map(op.sub, self.hidden_codes, self.current_guess)].count(0)
        # Azon jelzők száma, ahány esetben csak a kódérték helyes, de a pozíció nem.
        white_pegs = w if (w := (code_matches - black_pegs)) > 0 else 0
        self.black_pegs, self.white_pegs = black_pegs, white_pegs
        return black_pegs, white_pegs

    def check_state(self):
        """A játék aktuális állapotának ellenőrzése és ennek megfelelően az állapotváltozó beállítása. """
        # A játék sikeresen véget ér, ha mind a négy kód pozícióhelyesen megvan.
        if self.black_pegs == 4:
            self.state = GameState.WON
        # Ha az utolsó sorban sem lett megfejtés, akkor sikertelenül ér véget a játék.
        elif self.current_row_index + 1 == self.rowcount:
            self.state = GameState.LOST
        # Egyébként a játék folyamatban levő állapotban marad és az aktuális tippsort mutató változó értéke eggyel nő.
        else:
            self.current_row_index += 1
