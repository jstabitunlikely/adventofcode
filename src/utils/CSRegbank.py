class CSRegbank():

    def __init__(self,
                 regbank: dict[str, int] = {}) -> None:
        if regbank:
            self.regbank = regbank

    def set_regbank(self, regbank: dict[str, int] = {}) -> None:
        self.regbank = regbank

    def get_regbank(self) -> dict[str, int]:
        return self.regbank

    def get_register(self, register: str) -> int:
        return self.regbank[register]

    def set_register(self,
                     register: str,
                     value: int) -> None:
        self.regbank[register] = value
