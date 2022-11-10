class Light:

    on: bool

    def __init__(self):
        self.on = False

    def __str__(self) -> str:
        if self.on:
            return "Light is on."
        else:
            return "Light is off."
        
    def __bool__(self) -> bool:
        return self.on

    def switch(self) -> None:
        self.on = not self.on


if __name__ == "__main__":
    a: Light = Light()
    a.swtch()
    if bool(a):
        print(a)