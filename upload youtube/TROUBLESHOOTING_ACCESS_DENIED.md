# 🔧 Dépannage : Erreur access_denied même avec compte testeur

## Si votre compte est déjà dans la liste des testeurs mais que ça ne marche pas

### 1. Supprimer credentials.json pour forcer une nouvelle authentification

Le fichier `credentials.json` contient les tokens de l'ancienne authentification. Il faut le supprimer :

```bash
cd "/Users/terrybauer/Documents/site affiliation/itinero/upload youtube"
rm credentials.json
```

Ensuite, relancez le script. Cela forcera une nouvelle authentification avec votre compte.

### 2. Vérifier que vous utilisez le bon compte Google

Lors de l'authentification OAuth, assurez-vous de sélectionner le **même compte Google** que celui que vous avez ajouté dans Google Cloud Console comme testeur.

### 3. Vérifier le projet Google Cloud

Vérifiez que le projet Google Cloud correspond bien à votre fichier `client_secret_*.json` :
- Votre fichier actuel : `client_secret_557679969076-8232fsbd992jc6j1ttba4kbidbnd3or5.apps.googleusercontent.com.json`
- L'ID du projet commence par `557679969076`

Dans Google Cloud Console, vérifiez que vous êtes dans le **bon projet**.

### 4. Vérifier les scopes OAuth

Dans Google Cloud Console :
1. Allez dans **APIs & Services** > **OAuth consent screen**
2. Vérifiez que le scope `https://www.googleapis.com/auth/youtube.upload` est présent
3. Si ce n'est pas le cas, allez dans **Scopes** et ajoutez-le

### 5. Attendre quelques minutes

Parfois, les changements dans Google Cloud Console prennent quelques minutes à se propager. Attendez 5-10 minutes après avoir ajouté le testeur.

### 6. Vérifier l'état de l'application OAuth

Dans **OAuth consent screen**, vérifiez :
- **Publishing status** : Doit être "Testing" (pas "In production" qui nécessite une vérification)
- **Test users** : Votre email doit être listé
- **Scopes** : `youtube.upload` doit être présent

### 7. Utiliser un compte de test différent

Si vous avez plusieurs comptes Google, essayez avec un autre compte qui est également dans la liste des testeurs.

### 8. Vérifier les quotas YouTube

Vérifiez que vous n'avez pas atteint le quota YouTube (6 uploads par jour pour les comptes standard).

## Solution rapide

1. Supprimez `credentials.json` :
   ```bash
   cd "/Users/terrybauer/Documents/site affiliation/itinero/upload youtube"
   rm credentials.json
   ```

2. Relancez le script :
   ```bash
   python3 auto_upload_videos.py
   ```

3. Lors de l'authentification, sélectionnez **exactement le même compte** que celui dans la liste des testeurs.

4. Si ça ne marche toujours pas, vérifiez dans Google Cloud Console que :
   - Vous êtes dans le bon projet
   - Votre email est bien dans la liste des testeurs
   - Le scope `youtube.upload` est présent
