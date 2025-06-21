
# ElectriClim

*Gestion simplifiée de climatiseurs Tuya / SmartLife via une API et un dashboard web.*

---

## 🇫🇷 Présentation

**ElectriClim** est un système complet de gestion de climatiseurs compatibles Tuya (Smart Life).  
Grâce à son interface web intuitive et son API REST simple, vous pouvez contrôler vos climatiseurs sans passer par l'application officielle Smart Life.  

Il est idéal pour les passionnés de domotique qui souhaitent intégrer le contrôle de leurs climatiseurs dans leurs propres systèmes.

---

## 🇬🇧 Introduction

**ElectriClim** is a complete management system for Tuya-compatible air conditioners (Smart Life).  
With its intuitive web interface and simple REST API, you can control your air conditioners without using the official Smart Life app.  

It is ideal for smart home enthusiasts who want to integrate air conditioner control into their own systems.

---

## 🚀 Fonctionnalités principales / Main Features

- Dashboard web avec visualisation et contrôle en temps réel.  
  Web dashboard with real-time monitoring and control.
- API REST facile d’utilisation pour intégrer à vos scripts ou autres systèmes domotiques.  
  Easy-to-use REST API for integration with your scripts or other smart home systems.
- Commandes ON/OFF, réglage de la température, vitesse du ventilateur, et mode de fonctionnement.  
  ON/OFF commands, temperature setting, fan speed, and operation mode.
- Support multi-appareils avec configuration simple via un fichier `devices.json`.  
  Multi-device support with simple configuration via a `devices.json` file.
- Projet open-source développé en Python avec Flask et tinytuya.  
  Open-source project developed in Python with Flask and tinytuya.

---

## 🌐 API

Les commandes s’utilisent via des URL simples / Commands are used via simple URLs :

| Commande / Command            | Exemple URL / Example URL                 | Description                      |
|------------------------------|------------------------------------------|---------------------------------|
| Allumer la climatisation / ON | `/api/pseudo-clim/on`                     | Allumer l'appareil / Turn ON    |
| Éteindre la climatisation / OFF| `/api/pseudo-clim/off`                   | Éteindre l'appareil / Turn OFF  |
| Régler la température (°C) / Set Temp | `/api/pseudo-clim/set_temp=22`     | Définir la température / Set temperature |
| Régler la vitesse du ventilateur / Set Fan | `/api/pseudo-clim/set_fan=1`     | 0=auto, 1=low, 2=medium, 3=high |
| Régler le mode / Set Mode     | `/api/pseudo-clim/set_mode=1`             | 0=auto, 1=cool, 2=heat, 3=dry, 4=fan only |

*Remplacez `pseudo-clim` par le nom donné dans `devices.json`.*  
*Replace `pseudo-clim` with the name you gave in `devices.json`.*

---

## ⚙️ Installation / Installation

Un script d'installation automatisé est disponible ici : / Automated install script is available here:  
[https://electriummc.fr/tools/tools/electriclim/installer.sh](https://electriummc.fr/tools/tools/electriclim/installer.sh)

## ⚙️ Mis à jour / Update

Un script de mis à jour automatisé est disponible ici : / Automated update script is available here:  
[https://electriummc.fr/tools/tools/electriclim/update.sh](https://electriummc.fr/tools/tools/electriclim/update.sh)

### Prérequis / Requirements

- Python 3.6+ avec pip / Python 3.6+ with pip
- Accès root ou sudo pour l’installation / Root or sudo access for installation
- Compte Tuya IoT configuré (voir plus bas) / Tuya IoT account configured (see below)

### Étapes rapides / Quick steps

1. Cloner ou télécharger le projet. / Clone or download the project.
2. Lancer le script `installer.sh` en root : / Run the install script as root:  
   ```bash
   sudo bash installer.sh
   ```
3. Suivez les instructions pour configurer Tuya IoT et `devices.json`. / Follow instructions to configure Tuya IoT and `devices.json`.
4. Démarrez le service avec : / Start the service with:  
   ```bash
   ./start.sh
   ```
5. Accédez au dashboard via `http://<ip_serveur>:5000/` / Access the dashboard at `http://<server_ip>:5000/`

---

## 📱 Configuration Tuya IoT / Tuya IoT Configuration

Pour que ElectriClim fonctionne, vous devez / For ElectriClim to work, you must:

1. Créer un compte sur [https://iot.tuya.com](https://iot.tuya.com) / Create an account at [https://iot.tuya.com](https://iot.tuya.com)
2. Créer un projet Cloud, activer la plateforme Smart Life. / Create a Cloud project, enable Smart Life platform.
3. Lier votre compte Smart Life / Tuya à ce projet. / Link your Smart Life / Tuya account to this project.
4. Ajouter vos climatiseurs au compte Smart Life. / Add your air conditioners to the Smart Life account.
5. Récupérer les identifiants via `tinytuya wizard` (inclus dans l’install). / Retrieve device IDs using `tinytuya wizard` (included in install).

---

## 🛠️ Utilisation / Usage

- **Dashboard web** : contrôle en direct avec formulaire pour chaque appareil. / **Web dashboard**: live control form per device.
- **API REST** : utilisez les URL décrites ci-dessus. / **REST API**: use URLs described above.
- **Fichier `devices.json`** : modifiez pour ajouter/supprimer des appareils. / Edit `devices.json` to add/remove devices.

---

## 📦 Structure du projet / Project Structure

```
ElectriClim/
├── app.py              # Serveur Flask / Flask server
├── devices.json        # Configuration appareils / Devices config
├── start.sh            # Script de démarrage / Startup script
├── templates/
│   └── index.html      # Interface web / Web interface
└── static/
    └── style.css       # Styles CSS / CSS styles
```

---

## 💬 Support & contact

- Discord : **arthurgaming**  
- Site officiel & ressources : [https://electriummc.fr/tools/tools/electriclim/](https://electriummc.fr/tools/tools/electriclim/)

---

## 📝 Licence / License

Projet open-source / Open-source project — libre à vous de contribuer ou modifier. / Feel free to contribute or modify.

---

## Remerciements / Thanks

Merci à la communauté TinyTuya et Flask pour leurs outils. / Thanks to TinyTuya and Flask communities for their tools.

---

*Bonne gestion et bon confort avec ElectriClim !* / *Enjoy managing your climate comfort with ElectriClim!*  
— Arthur
