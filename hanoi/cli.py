"""Console interface; all tower numbers shown to users are one-based."""

from .game import Game
from .scores import ScoreStore
from .solver import solve


def run(store=None):
    store = store or ScoreStore()
    print("Tours de Hanoï — déplacer tous les disques sur la tour 3.")
    while True:
        try:
            game = Game(
                int(input("Nombre de disques (1–10) : ")), input("Mode défi ? (oui/non) : ").strip().lower() == "oui"
            )
        except ValueError as error:
            print(error)
            continue
        while True:
            print(game.towers, f"Coups : {game.moves} / minimum : {game.minimum}")
            if game.won:
                print("Victoire !")
                try:
                    store.add(input("Nom : "), game)
                except (ValueError, OSError) as error:
                    print(f"Score non enregistré : {error}")
                break
            if game.exhausted:
                print("Limite atteinte. Vous pouvez annuler ou recommencer.")
            action = input("Déplacement « 1 3 », annuler, solution, scores, nouvelle ou quitter : ").strip().lower()
            try:
                if action == "quitter":
                    return
                if action == "nouvelle":
                    break
                if action == "annuler":
                    game.undo()
                elif action == "solution":
                    demo = Game(game.disks)
                    for source, target in solve(game.disks):
                        demo.move(source, target)
                        print(f"{source + 1} → {target + 1} : {demo.towers}")
                    print("Démonstration terminée ; votre partie est conservée.")
                elif action == "scores":
                    for row in store.ranking():
                        print(f"{row['disks']} disques · {row['name']} · {row['moves']} coups")
                else:
                    source, target = map(int, action.split())
                    game.move(source - 1, target - 1)
            except (ValueError, OSError) as error:
                print(error)
        if input("Rejouer ? (oui/non) : ").strip().lower() != "oui":
            return
