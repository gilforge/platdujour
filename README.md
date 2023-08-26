# Plat du jour
- **Plat du jour** est une application qui génère aléatoirement une liste de 14 repas (deux repas par jour : midi et soir) à partir d'une base de données de vos plats préférés. Vous pouvez refuser les plats proposés, l'application vous en propose un nouveau.
- Une fois la liste accepté, vous pouvez l'exporter en PDF.

# Mode d'emploi
- En exécutant le fichier vous obtenez la liste des 7 jours de la semaine (commençant par le lundi) et le moment de la journée (midi ou soir) soit 14 lignes. Par défaut, **PlatDuJour** pré-rempli les jours de 14 propositions aléatoires.
- Si vous cliquer sur *refuser*, **PlatDuJour** vous fait immédiatement une nouvelle proposition, tirée de votre BDD.
- Une fois que la liste vous convient, vous pouvez l'exporter en PDF et l'emmener avec vous pour faire vos courses (sur le marché, par exemple).

# La base de données
- Vous pouvez créer un fichier tableur (libreoffice, excel, google sheet, etc.) que vous mettez à jour avec vos dernières découvertes, puis vous l'exporter en CSV pour l'utiliser avec **Plat Du Jour**. N'oubliez pas de placer le CSV dans le même répertoire que l'exécutable **PlatDuJour.exe**.
- Dans le tableau, la 1ère colonne indique vos préférences. Vous pourriez aimer manger un plat le midi, le soir ou le manger aux deux repas. Vous saisirez donc : m (pour midi), s (pour soir), ms (pour midi ou soir).
- La seconde colonne est la désignation du plat : Kebab maison, pizza à l'ananas (^_^), etc. 

# Installation
- Décompressez le fichier ZIP
- Double cliquez sur le fichier exécutable.# Liste des fichiers

# Versions
- 0.0.1 > Mise à disposition fonctionnelle (1er jet).