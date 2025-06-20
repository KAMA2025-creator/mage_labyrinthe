import socket
import subprocess
import re
from datetime import datetime

tentatives_invalides = 0  # 🔐 Compteur de domaines invalides

while True:
    resultat_final = []
    domaine = input("Entrez un nom de domaine (ou tapez 'exit' pour quitter) : ").strip()

    if domaine.lower() == "exit":
        print("👋 Merci d’avoir utilisé CYBERSCAN PRO+ ! À bientôt.")
        break

    try:
        ip = socket.gethostbyname(domaine)
        tentatives_invalides = 0  # ✅ Domaine correct → on réinitialise
        resultat_final.append(f"L'adresse IP de {domaine} est : {ip}")

        # PING
        reussites = 0
        for i in range(3):
            resultat = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.DEVNULL)
            if resultat.returncode == 0:
                reussites += 1
        pourcentage = (reussites / 3) * 100
        resultat_final.append(f"{reussites}/3 pings réussis ({pourcentage:.0f}%)")
        if reussites == 0:
            resultat_final.append(" Aucune réponse au ping (peut être bloqué par un pare-feu)")

        # TTL
        resultat = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True)
        texte_ping = resultat.stdout
        match = re.search(r"TTL=(\d+)", texte_ping, re.IGNORECASE)
        if match:
            ttl = int(match.group(1))
            resultat_final.append(f"TTL reçu : {ttl}")
            if 0 < ttl <= 64:
                resultat_final.append("Probablement Linux ")
            elif 65 <= ttl <= 128:
                resultat_final.append("Probablement Windows ")
            elif ttl > 128:
                resultat_final.append("Probablement Cisco ou équipement réseau ")
            else:
                resultat_final.append("Impossible de deviner le système")

        # Résolution inverse
        try:
            nom_machine = socket.gethostbyaddr(ip)[0]
            resultat_final.append(f"Résolution inverse : {ip} → {nom_machine}")
        except socket.herror:
            resultat_final.append("Aucun nom associé à cette adresse IP.")

        # Bannières
        def lire_banniere(ip, port):
            try:
                prise = socket.socket()
                prise.settimeout(2)
                prise.connect((ip, port))
                banniere = prise.recv(1024).decode(errors="ignore")
                prise.close()
                return banniere.strip()
            except:
                return "Pas de bannière ou non lisible"

        # Scan ports
        ports = [22, 80, 443, 3306]
        ports_ouverts = []
        resultat_final.append(" Scan des ports en cours...")
        for port in ports:
            prise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            prise.settimeout(1)
            result = prise.connect_ex((ip, port))
            if result == 0:
                ports_ouverts.append(port)
                resultat_final.append(f" Port {port} ouvert")
                banniere = lire_banniere(ip, port)
                resultat_final.append(f"   → {banniere}")
            else:
                resultat_final.append(f"Port {port} fermé")
            prise.close()

        # Requête HTTP
        def requete_http(domaine):
            try:
                prise = socket.socket()
                prise.settimeout(3)
                prise.connect((ip, 80))
                requete = f"GET / HTTP/1.1\r\nHost: {domaine}\r\n\r\n"
                prise.send(requete.encode())
                reponse = prise.recv(1024).decode(errors="ignore")
                prise.close()
                resultat_final.append("📝 Réponse HTTP :")
                resultat_final.append(reponse.strip())
            except:
                resultat_final.append("❌ Échec de la requête HTTP.")
        requete_http(domaine)

        # Scan sous-domaines
        def scanner_sous_domaines(domaine):
            sous_domaines = ["www", "mail", "admin", "ftp", "webmail", "dev", "vpn"]
            resultat_final.append("\n🔎 Scan des sous-domaines connus :")
            for prefixe in sous_domaines:
                sous_domaine = f"{prefixe}.{domaine}"
                try:
                    ip_sous = socket.gethostbyname(sous_domaine)
                    resultat_final.append(f"✅ {sous_domaine} → {ip_sous}")
                except socket.gaierror:
                    resultat_final.append(f"❌ {sous_domaine} introuvable")
        scanner_sous_domaines(domaine)

        # Rapport
        def generer_rapport(domaine, contenu):
            nom_fichier = f"rapport_{domaine.replace('.', '_')}.txt"
            try:
                with open(nom_fichier, "w", encoding="utf-8") as fichier:
                    fichier.write(contenu)
                print(f"\n📄 Rapport enregistré sous : {nom_fichier}")
            except Exception as e:
                print(f"Erreur lors de la génération du rapport : {e}")
        generer_rapport(domaine, "\n".join(resultat_final))

        # Historique
        def enregistrer_historique(domaine, ip, ports_ouverts):
            date_scan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ports_str = ", ".join(str(p) for p in ports_ouverts) if ports_ouverts else "aucun port ouvert"
            ligne = f"[{date_scan}] Domaine : {domaine} | IP : {ip} | Ports ouverts : {ports_str}\n"
            try:
                with open("historique.txt", "a", encoding="utf-8") as fichier:
                    fichier.write(ligne)
                print("🗃️ Historique mis à jour.")
            except Exception as e:
                print(f"Erreur lors de la mise à jour de l'historique : {e}")
        enregistrer_historique(domaine, ip, ports_ouverts)

        # ASCII
        etat_ports = ["■" if port in ports_ouverts else "□" for port in ports]
        ascii_ports = f"\nPorts scannés : {ports}\nÉtat          : {etat_ports}"
        resultat_final.append(ascii_ports)

        # Clôture
        print("\n✅ Scan terminé avec succès !")
        print(f"📄 Rapport disponible : rapport_{domaine.replace('.', '_')}.txt")
        print("📂 L’historique du scan a été mis à jour dans 'historique.txt'")
        print("🕒 Fin de l’analyse réseau.")
        print("Merci d’avoir utilisé CYBERSCAN PRO+ 🔐")

    except socket.gaierror:
        tentatives_invalides += 1
        print("⛔ Domaine invalide ou introuvable.")
        if tentatives_invalides >= 3:
            print("🚫 3 domaines invalides consécutifs. Fin du programme.")
            break
        
