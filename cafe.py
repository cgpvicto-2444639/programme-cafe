from abc import ABC

# Source : https://refactoring.guru/fr/design-patterns/mediator/python/example
class Mediateur(ABC):
    """
    Interface abstraite du Médiateur est le composant principal qui réagit avec tout les autres composants.
    Définit le notify par lequel tous les composants signalent des évènements sans connaître les autres.
    """

    def notify(self, sender: object, event: str) -> None:
        pass

class MediateurCafetiereConcret(Mediateur):
    """
    Amène le cerveau de l'application, il connaît tous les composants et centralise toute la logique de coordination
    et les règles métier (ex: vérifier si la machine est allumée avant de pouvoir couler le café)
    """
    def __init__(self, machine: 'MachineACafe', cafe: 'Cafe', sucre: 'Sucre', tasse: 'Tasse') -> None:
        self._machine = machine
        self._machine.mediateur = self
        self._cafe = cafe
        self._cafe.mediateur = self
        self._sucre = sucre
        self._sucre.mediateur = self
        self._tasse = tasse
        self._tasse.mediateur = self

    def notify(self, sender: object, event: str) -> None:
        """
        Gère les évènements reçus depuis les composants et groupe les actions
        """
        if event == "demarrer_machine":
            if self._machine.is_on:
                print("[Médiateur] La machine est allumée. Prête à servir !")
            else:
                print("[Médiateur] La machine est éteinte.")

        elif event == "demande_cafe":
            # Règle métier n1: On ne peut pas faire de café si la machine est éteinte
            if not self._machine.is_on:
                print("[Médiateur] impossible de faire du café, la machine est éteinte !")
                return
            
            print("[Médiateur] Préparation du café :")
            self._tasse.placer()
            self._cafe.couler()
            print("[Médiateur] Le café est prêt dans la tasse !")

        elif event == "demande_sucre":
            # Règle métier n2: Vérifie si une tasse est présente pour recevoir le sucre
            if not self._tasse.presente:
                print("[Médiateur] Impossible d'ajouter du sucre, il n'y a pas de tasse !")
                return
            
            self._sucre.ajouter()
        

class BaseComponent:
    """
    Le classe de base pour tous les composants de la machine. Elle fournit une référence
    partagée vers le médiateur
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
Les composants concrets implémentent différentes fonctionnalités. Ils ne dépendant pas sur les autres composants.
"""

class MachineACafe(BaseComponent):
    def __init__(self) -> None:
        super().__init__()
        self.is_on = False

    def basculer_alimentation(self) -> None:
        self.is_on = not self.is_on
        print(f"[MachineACafe] Alimentation basculée (État : {self.is_on})")
        self.mediateur.notify(self, "demarrer_machine")

class Cafe(BaseComponent):
    def couler(self) -> None:
        print("[Cafe] Le café coule dans la tasse (50ml).")
        
class Sucre(BaseComponent):
    def __init__(self) -> None:
        super().__init__()
        self.quantite = 0

    def ajouter(self) -> None:
        self.quantite += 10
        print(f"[Sucre] Ajout de 10g de sucre (Total : {self.quantite}g).")

class Tasse(BaseComponent):
    def __init__(self) -> None:
        super().__init__()
        self.presente = True

    def placer(self) -> None:
        print("[Tasse] Tasse bien positionnée.")
         
# Source : https://medium.com/@anushagrawal01/building-an-interactive-python-menu-for-executing-commands-2e8a6b028a38
def afficher_menu():
    print(" == Menu de la Machine à Café ==")
    print("1. Allumer ou Éteindre la machine")
    print("2. Faire un café (Action coordonnée : Tasse + Café)")
    print("3. Ajout de sucre dans le café (Interagit avec la tasse et le café)")
    print("4. Quitter")

if __name__ == "__main__":
    machine = MachineACafe()
    cafe = Cafe()
    sucre = Sucre()
    tasse = Tasse()

    mediateur = MediateurCafetiereConcret(machine, cafe, sucre, tasse)

    while True:
        print("\n")
        afficher_menu()
        choix = input("Choisissez une option pour le choix de votre café (1-4) : ").strip()

        print()

        if choix == "1":
            machine.basculer_alimentation()
        elif choix == "2":
            machine.mediateur.notify(machine, "demande_cafe")
        elif choix == "3":
            sucre.mediateur.notify(sucre, "demande_sucre")
        elif choix == "4":
            print("Au revoir!")
            break
        else:
            print("[Erreur]  Choix invalide, veuillez entrer 1, 2, 3 ou 4.")


    