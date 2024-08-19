from pyzf.interfaces import Interface, default_method, implements, method, optional_method


class Jedi(Interface):
    @method
    def speak(self) -> str:
        pass

    @method
    def force_power(self) -> int:
        pass

    @default_method
    def default_greet(self) -> str:
        return f"May the Force be with you. I am {self.speak()}"


class Sith(Interface):
    @method
    def force_lightning(self) -> None:
        pass

    @optional_method
    def optional_force_choke(self) -> None:
        pass


class ForceUser(Jedi, Sith):
    pass


@implements(ForceUser)
class DarthVader:
    def speak(self) -> str:
        return "I am Darth Vader, Dark Lord of the Sith"

    def force_power(self) -> int:
        return 950

    def force_lightning(self) -> None:
        print("⚡️ Force Lightning!")


def use_the_force(obj: ForceUser):
    print(f"Type of obj: {type(obj)}")
    print(obj.default_greet())


vader = DarthVader()
print(vader.speak())
print(vader.force_power())

use_the_force(vader)
vader.force_lightning()
