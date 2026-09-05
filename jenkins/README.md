# Jenkins local

Depuis la racine du projet :

```powershell
docker compose -f jenkins-compose.yml up -d --build
```

Jenkins est disponible sur http://localhost:8080.

Recuperer le mot de passe initial :

```powershell
docker exec typhoon-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Creer ensuite un job **Pipeline**, choisir **Pipeline script from SCM**, renseigner :

- SCM : Git
- Repository : `https://github.com/leouss774/Typhoon2-Alpha.git`
- Branch : `*/main` (ou la branche a tester)
- Script Path : `Jenkinsfile`

Le conteneur Jenkins monte `/var/run/docker.sock` et contient Docker CLI + Docker Compose, ce qui permet au Jenkinsfile de construire les images du projet avec le daemon Docker Desktop.

Pour arreter Jenkins :

```powershell
docker compose -f jenkins-compose.yml down
```
