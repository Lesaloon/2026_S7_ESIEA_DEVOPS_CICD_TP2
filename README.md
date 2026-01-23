# TP CICD 2

pour lancer la pipeline il faut commiter un changement sur une branche et ouvrir une Pull Request vers la branche main.

la branche main est normalement protégée et ne peut pas recevoir de push direct.

```
on:
  # Le pipeline s’exécute à chaque Pull Request
  pull_request:
  # Le pipeline s’exécute aussi à chaque push sur la branche main
  push:
    branches: [main]
```

cellon les policy définies dans les settings du repo, la PR peut nécésiter que la pipeline soit passée avec succès avant de pouvoir être mergée.
il est possible que ce ne soit pas le cas, mais ce n'est pas recommandé.
