from abc import ABC

# Source : https://refactoring.guru/fr/design-patterns/mediator/python/example
class Mediateur(ABC):
    """
    Le médiateur est le composant principal qui réagit avec tout les autres composants.
    """

    def notify(self, sender: object, event: str) -> None:
        pass

class MediateurConcret(Mediateur):
    def __init__(self, component1: Composant1, component2: Composant2) -> None:
        self._component1 = component1
        self._component1.mediateur = self
        self._component2 = component2
        self._component2.mediateur = self

    def notify(self, sender: object, event: str) -> None:
        if event == "Allumer/Éteindre":
            print("Mediateur réagit au A et trigger les opérations suivantes:")
            self._component2.do_c()
        elif event == "Café court":
            print("Médiateur réagit au D et trigger les opérations suivantes:")
            self._component2.do_c()
        elif event == "Ajout sucre":
            print("Médiateur réagit au B")

class BaseComponent:
    """
    Le composant de base donne les fonctionnalités de base de sorte un médiator instance dans des objets de composants.
    """

    def __init__(self, mediateur: Mediateur = None) -> None:
        self._mediateur = mediateur

    @property
    def mediateur(self) -> Mediateur:
        return self._mediateur
    
    @mediateur.setter
    def mediateur(self, mediateur: Mediateur) -> None:
        self._mediateur = mediateur

"""
Les composants concrets implémentent différentes fonctionnalités. Ils ne dépendant pas sur les autres components.
Ils ne dépendant pas non plus sur les classes de médiateur concrets.
"""

class Composant1(BaseComponent):
    def __init__(self, mediateur: Mediateur = None) -> None:
        super().__init__(mediateur)
        self.is_on = False
        self.quantite_sucre = 0

    def do_a(self) -> None:
        self.is_on = not self.is_on
        print(f"Composant 1 fait A (État: {self.is_on})")
        self.mediateur.notify(self, "Allumer/Éteindre")

    def do_b(self) -> None:
        self.quantite_sucre += 10
        print(f"Composant 1 fait B (Ajout de sucre {self.quantite_sucre}g)")
        self.mediateur.notify(self, "Ajout sucre")

class Composant2(BaseComponent):
    def __init__(self, mediateur: Mediateur = None) -> None:
        self.mil_cafe = 50

    def do_c(self) -> None:
        print("Composant 2 fait C")
        self.mediateur.notify(self, "C")

    def do_d(self) -> None:
        print(f"Composant 2 fait D (Café court ajouté) {self.mil_cafe}ml")
        self.mediateur.notify(self, "Café court")
        
# Source : https://medium.com/@anushagrawal01/building-an-interactive-python-menu-for-executing-commands-2e8a6b028a38
def afficher_menu():
    print(" == Menu du café (Médiateur) ==")
    print("1. Change l'état de la machine pour Allumer ou Éteindre (Déclencher opération A)")
    print("2. Demande un café court (Déclencher opération D)")
    print("3. Ajout de sucre dans le café (Déclencher opération B)")
    print("4. Quitter")

if __name__ == "__main__":
    c1 = Composant1()
    c2 = Composant2()
    mediateur = MediateurConcret(c1, c2)

    while True:
        print("\n")
        afficher_menu()
        choix = input("Choisissez une option pour le choix de votre café (1-4) : ").strip()

        print()

        if choix == "1":
            print("--- Le client déclenche opération A (Allumer ou éteindre la machine à café) ---")
            c1.do_a()
        elif choix == "2":
            print("--- Le client déclenche opération D (Demande un café court) ---")
            c2.do_d()
        elif choix == "3":
            print("--- Le client déclenche opération B (Ajout de sucre) ---")
            c1.do_b()
        elif choix == "4":
            print("Au revoir!")
            break
        else:
            print("[Erreur]  Choix invalide, veuillez entrer 1, 2, 3 ou 4.")


    