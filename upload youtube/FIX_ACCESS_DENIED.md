# 🔧 Solution : Erreur "Access Denied" - Application en mode test

## Problème
Vous voyez cette erreur :
```
Accès bloqué : upload youtube n'a pas terminé la procédure de validation de Google
Erreur 403 : access_denied
```

## Cause
L'application OAuth est en mode "test" dans Google Cloud Console. Seuls les comptes de test approuvés peuvent y accéder.

## Solution : Ajouter votre compte comme testeur

### Option 1 : Ajouter votre compte dans Google Cloud Console (RECOMMANDÉ)

1. **Accéder à Google Cloud Console** :
   - Allez sur : https://console.cloud.google.com/
   - Sélectionnez le projet correspondant à votre `client_secret_*.json`

2. **Naviguer vers l'écran de consentement OAuth** :
   - Dans le menu de gauche, allez dans **"APIs & Services"** > **"OAuth consent screen"**
   - Ou directement : https://console.cloud.google.com/apis/credentials/consent

3. **Ajouter des utilisateurs de test** :
   - Dans la section **"Test users"**, cliquez sur **"+ ADD USERS"**
   - Ajoutez l'adresse email du compte Google que vous utilisez pour YouTube
   - Cliquez sur **"ADD"**

4. **Relancer le script** :
   - Relancez `python3 auto_upload_videos.py`
   - Connectez-vous avec le compte Google que vous venez d'ajouter

### Option 2 : Passer en mode "Production" (nécessite vérification Google)

⚠️ **Attention** : Pour passer en mode production, Google peut demander une vérification de l'application, ce qui peut prendre plusieurs jours/semaines.

1. Dans **"OAuth consent screen"**, changez le mode de **"Testing"** à **"In production"**
2. Si demandé, remplissez le formulaire de vérification Google
3. Attendez l'approbation de Google

### Option 3 : Utiliser un compte de test existant

Si vous avez déjà un compte qui fonctionne, utilisez-le pour l'authentification.

## Vérification

Après avoir ajouté votre compte comme testeur :
1. Supprimez `credentials.json` si il existe (pour forcer une nouvelle authentification)
2. Relancez le script d'upload
3. Vous devriez pouvoir vous connecter avec votre compte

## Note importante

- Vous pouvez ajouter jusqu'à **100 comptes de test** dans Google Cloud Console
- Les comptes de test ont accès pendant 7 jours, après quoi ils doivent se ré-authentifier
- Pour éviter les limitations, passez en mode production (nécessite vérification Google)
